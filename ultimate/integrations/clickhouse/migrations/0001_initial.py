from django_clickhouse import migrations
from ultimate.integrations.clickhouse.models import Event, Person, Element

class Migration(migrations.Migration):
    operations = [
        migrations.CreateTable(Event),
        migrations.CreateTable(Person),
        migrations.CreateTable(Element)
    ]
