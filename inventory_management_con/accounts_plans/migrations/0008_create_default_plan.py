# accounts/migrations/000X_create_default_plan.py
from django.db import migrations

def create_default_plan(apps, schema_editor):
    Plan = apps.get_model('accounts_plans', 'Plan')
    if not Plan.objects.filter(is_default=True).exists():
        Plan.objects.create(
            plan_name="Default Plan",
            plan_description="This is the default plan.",
            warehouse_limit=1,
            category_per_warehouse_limit=3,
            products_per_category_limit=20,
            price=None,
            is_default=True,
            plan_type="monthly"
        )

class Migration(migrations.Migration):

    dependencies = [
        ('accounts_plans', '0007_plan_plan_type'),  # Örneğin '0001_initial' migrasyonu
    ]

    operations = [
        migrations.RunPython(create_default_plan),
    ]
