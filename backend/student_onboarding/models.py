import uuid
from django.db import models

class StudentOnboarding(models.Model):
    """
    Student Onboarding Model.
    Stores raw evaluation metrics alongside DCYN (Discretized Binary Yes/No) flags.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student_name = models.CharField(max_length=150)
    age = models.IntegerField(help_text="Student age (Must be 3 to 18)")
    evaluation_score = models.FloatField(help_text="Diagnostic assessment score (0.0 to 100.0)")
    
    # Raw parent consent input
    parent_consent_given = models.BooleanField(default=False)
    guardian_email = models.EmailField()

    # Task 3: DCYN (Discretized Binary Yes/No) Logic Library Fields (1 = Yes, 0 = No)
    dcyn_has_parent_consent = models.IntegerField(
        choices=[(1, 'Yes'), (0, 'No')],
        help_text="DCYN Binary Flag: 1 = Parent Consent Verified, 0 = No Consent"
    )
    dcyn_requires_lsa_support = models.IntegerField(
        choices=[(1, 'Yes'), (0, 'No')],
        help_text="DCYN Binary Flag: 1 = LSA Support Required (Score < 70), 0 = Standard Support"
    )
    dcyn_is_eligible_for_program = models.IntegerField(
        choices=[(1, 'Yes'), (0, 'No')],
        help_text="DCYN Binary Flag: 1 = Program Eligible (Age 3-18 & Parent Consent), 0 = Ineligible"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} (Age: {self.age}, DCYN Eligible: {self.dcyn_is_eligible_for_program})"
