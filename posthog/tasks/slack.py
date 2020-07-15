from celery import shared_task
from django.apps import apps
from django.conf import settings
import re
import requests

@shared_task
def post_event_to_slack(event_id: int, site_url: str) -> None:
    # must import "Event" like this to avoid circular dependency with models.py (it imports tasks.py)
    event_model = apps.get_model(app_label="posthog", model_name="Event")
    event = event_model.objects.get(pk=event_id)
    team = event.team

    if not site_url:
        site_url = settings.SITE_URL

    if team.slack_incoming_webhook:
        try:
            user_name = event.person.properties.get("email", event.distinct_id)
        except:
            user_name = event.distinct_id

        webhook_type = "teams"
        if "slack.com" in team.slack_incoming_webhook:
            webhook_type = "slack"

        if webhook_type == "slack":
            user_markdown = "<{}/person/{}|{}>".format(site_url, event.distinct_id, user_name)

        else:
            user_markdown = "[{}]({}/person/{})".format(user_name, site_url, event.distinct_id)

        actions = [action for action in event.action_set.all() if action.post_to_slack]
        if actions:
            for action in actions:
                message_format = action.slack_message_format
                matched_tokens = re.findall(r"(?<=\[)(.*?)(?=\])", message_format)

                if matched_tokens:
                    action_message = re.sub(r"\[(.*?)\]", '{}', message_format)
                    replaced_tokens = []
                    replaced_markdown_tokens = []

                    if webhook_type == "slack":
                        action_markdown = '"<{}/action/{}|{}>"'.format(site_url, action.id, action.name)
                    else:
                        action_markdown = '"[{}]({}/action/{})"'.format(action.name, site_url, action.id)

                    for token in matched_tokens:
                        token_type = re.findall(r"\w+", token)[0]
                        token_prop = re.findall(r"\w+", token)[1]

                        
                        try:
                            if token_type == "user":
                                if token_prop == "name":
                                    replaced_markdown_tokens.append(user_markdown)
                                    replaced_tokens.append(user_name)
                                else:
                                    user_property = event.properties.get("$" + token_prop)
                                    if user_property is None:
                                        raise ValueError

                                    replaced_markdown_tokens.append(user_property)
                                    replaced_tokens.append(user_property)

                            elif token_type == "action":
                                if token_prop == "name":

                                    replaced_tokens.append(action.name)
                                    replaced_markdown_tokens.append(action_markdown)

                            elif token_type == "event":
                                if token_prop == "name":
                                    replaced_tokens.append(event.event)
                                    replaced_markdown_tokens.append(event.event)

                            message_markdown = action_message.format(*replaced_markdown_tokens)
                            message_text = action_message.format(*replaced_tokens)
                        except:
                            error_message = "⚠ Error: There are one or more formatting errors in the slack message template for action {}."
                            message_text = error_message.format("\"" + action.name + "\"")
                            message_markdown = error_message.format(action_markdown)

                    if webhook_type == "slack":
                        message = {
                            "text": message_text,
                            "blocks": [
                                {
                                    "type": "section",
                                    "text": {
                                        "type": "mrkdwn",
                                        "text": message_markdown,
                                    },
                                }
                            ],
                        }
                    else:
                        message = {
                            "text": message_markdown,
                        }
                    requests.post(team.slack_incoming_webhook, verify=False, json=message)
