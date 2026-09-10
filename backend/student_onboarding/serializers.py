# ==============================================================================
# Task 3: Schema Mapping & DCYN (Discretized Binary Yes/No) Serializer
# ==============================================================================
# Position: Junior Cloud & DevOps Engineer (GCP / Django / React)
# Purpose: Deconstructs raw incoming student onboarding JSON payload into
# deterministic binary Yes/No (1/0) flags to eliminate human judgment in data pipelines.
# ==============================================================================

from rest_framework import serializers
from .models import StudentOnboarding


class StudentOnboardingSerializer(serializers.ModelSerializer):
    """
    Serializer enforcing exact boundary validations and generating DCYN binary logic flags.
    """

    # Input validation thresholds (Poka-Yoke mistake-proofing)
    MIN_AGE = 3
    MAX_AGE = 18
    MIN_SCORE = 0.0
    MAX_SCORE = 100.0
    LSA_SUPPORT_THRESHOLD_SCORE = 70.0  # Scores below 70 require LSA support

    # Read-only DCYN binary logic fields produced automatically
    dcyn_has_parent_consent = serializers.IntegerField(read_only=True)
    dcyn_requires_lsa_support = serializers.IntegerField(read_only=True)
    dcyn_is_eligible_for_program = serializers.IntegerField(read_only=True)

    class Meta:
        model = StudentOnboarding
        fields = [
            'id',
            'student_name',
            'age',
            'evaluation_score',
            'parent_consent_given',
            'guardian_email',
            'dcyn_has_parent_consent',
            'dcyn_requires_lsa_support',
            'dcyn_is_eligible_for_program',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def validate_age(self, value):
        """Strict validation limit for student age."""
        if value < self.MIN_AGE or value > self.MAX_AGE:
            raise serializers.ValidationError(
                f"Invalid Age: {value}. Age must be between {self.MIN_AGE} and {self.MAX_AGE} years."
            )
        return value

    def validate_evaluation_score(self, value):
        """Strict validation limit for diagnostic assessment score."""
        if value < self.MIN_SCORE or value > self.MAX_SCORE:
            raise serializers.ValidationError(
                f"Invalid Evaluation Score: {value}. Score must be between {self.MIN_SCORE} and {self.MAX_SCORE}."
            )
        return value

    def validate(self, attrs):
        """
        Executes DCYN (Discretized Binary Yes/No) Logic Library Mapping:
        ------------------------------------------------------------------
        - DCYN Flag 1 (Parent Consent): 1 if consent_given is True, else 0.
        - DCYN Flag 2 (Requires LSA Support): 1 if score < 70.0, else 0.
        - DCYN Flag 3 (Program Eligibility): 1 if age is valid AND consent is True, else 0.
        """
        age = attrs.get('age')
        score = attrs.get('evaluation_score')
        consent = attrs.get('parent_consent_given', False)

        # 1. DCYN Binary Mapping: Parent Consent
        dcyn_consent = 1 if consent else 0

        # 2. DCYN Binary Mapping: LSA Support Requirement (Deterministic threshold logic)
        dcyn_lsa_required = 1 if score < self.LSA_SUPPORT_THRESHOLD_SCORE else 0

        # 3. DCYN Binary Mapping: Absolute Program Eligibility Rule
        is_age_valid = (self.MIN_AGE <= age <= self.MAX_AGE)
        dcyn_eligible = 1 if (is_age_valid and consent) else 0

        # Inject DCYN binary library outputs into validated attributes
        attrs['dcyn_has_parent_consent'] = dcyn_consent
        attrs['dcyn_requires_lsa_support'] = dcyn_lsa_required
        attrs['dcyn_is_eligible_for_program'] = dcyn_eligible

        return attrs

    def create(self, validated_data):
        """Persists validated model with calculated DCYN binary flags."""
        return StudentOnboarding.objects.create(**validated_data)
