# Generated initial migration for student_onboarding model

import uuid
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StudentOnboarding',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('student_name', models.CharField(max_length=150)),
                ('age', models.IntegerField(help_text='Student age (Must be 3 to 18)')),
                ('evaluation_score', models.FloatField(help_text='Diagnostic assessment score (0.0 to 100.0)')),
                ('parent_consent_given', models.BooleanField(default=False)),
                ('guardian_email', models.EmailField(max_length=254)),
                ('dcyn_has_parent_consent', models.IntegerField(choices=[(1, 'Yes'), (0, 'No')], help_text='DCYN Binary Flag: 1 = Parent Consent Verified, 0 = No Consent')),
                ('dcyn_requires_lsa_support', models.IntegerField(choices=[(1, 'Yes'), (0, 'No')], help_text='DCYN Binary Flag: 1 = LSA Support Required (Score < 70), 0 = Standard Support')),
                ('dcyn_is_eligible_for_program', models.IntegerField(choices=[(1, 'Yes'), (0, 'No')], help_text='DCYN Binary Flag: 1 = Program Eligible (Age 3-18 & Parent Consent), 0 = Ineligible')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
