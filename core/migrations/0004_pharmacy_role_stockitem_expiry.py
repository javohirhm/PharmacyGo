from django.db import migrations, models


def forwards(apps, schema_editor):
    Profile = apps.get_model("core", "Profile")
    Notification = apps.get_model("core", "Notification")
    Profile.objects.filter(role="doctor").update(role="pharmacy")
    Notification.objects.filter(audience="doctor").update(audience="pharmacy")


def backwards(apps, schema_editor):
    Profile = apps.get_model("core", "Profile")
    Notification = apps.get_model("core", "Notification")
    Profile.objects.filter(role="pharmacy").update(role="doctor")
    Notification.objects.filter(audience="pharmacy").update(audience="doctor")


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_order_items_order_progress"),
    ]

    operations = [
        migrations.AddField(
            model_name="stockitem",
            name="expires_in_days",
            field=models.PositiveIntegerField(default=30),
        ),
        migrations.AlterField(
            model_name="notification",
            name="audience",
            field=models.CharField(
                choices=[
                    ("admin", "Admin"),
                    ("customer", "Customer"),
                    ("distributor", "Distributor"),
                    ("pharmacy", "Pharmacy store"),
                ],
                default="customer",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="role",
            field=models.CharField(
                choices=[
                    ("admin", "Admin"),
                    ("customer", "Customer"),
                    ("distributor", "Distributor"),
                    ("pharmacy", "Pharmacy store"),
                ],
                default="customer",
                max_length=20,
            ),
        ),
        migrations.RunPython(forwards, backwards),
    ]
