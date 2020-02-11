from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.apps import apps
from posthog.models import User, Team, Funnel, FunnelStep, Action, ActionStep, DashboardItem, Event, Person, Element

admin.site.register(Team)
admin.site.register(Funnel)
admin.site.register(FunnelStep)
admin.site.register(Action)
admin.site.register(ActionStep)
admin.site.register(DashboardItem)

if not hasattr(settings, 'EVENTS_MODELS'):
    admin.site.register(Person)
    admin.site.register(Element)
    @admin.register(Event)
    class EventAdmin(admin.ModelAdmin):
        readonly_fields = ('timestamp',)
        list_display = ('timestamp', 'event', 'id',)

        def get_queryset(self, request):
            qs = super(EventAdmin, self).get_queryset(request)
            return qs.order_by('-timestamp')
 
@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""
    change_form_template = 'loginas/change_form.html'

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('PostHog'), {'fields': ('temporary_token', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)