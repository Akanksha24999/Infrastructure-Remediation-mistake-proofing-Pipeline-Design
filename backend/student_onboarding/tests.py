from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .serializers import StudentOnboardingSerializer

class DCYNSerializerTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_valid_payload_generates_dcyn_flags(self):
        """Verify valid payload generates correct binary Yes/No flags (1/0)."""
        payload = {
            "student_name": "Alexander Smith",
            "age": 8,
            "evaluation_score": 58.5,  # < 70 -> Requires LSA support
            "parent_consent_given": True,
            "guardian_email": "parent@example.com"
        }
        serializer = StudentOnboardingSerializer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        data = serializer.validated_data
        
        self.assertEqual(data['dcyn_has_parent_consent'], 1)
        self.assertEqual(data['dcyn_requires_lsa_support'], 1)
        self.assertEqual(data['dcyn_is_eligible_for_program'], 1)

    def test_high_score_lsa_support_flag(self):
        """Verify score >= 70 yields dcyn_requires_lsa_support = 0."""
        payload = {
            "student_name": "Emma Watson",
            "age": 12,
            "evaluation_score": 85.0,  # >= 70 -> No LSA support required
            "parent_consent_given": True,
            "guardian_email": "emma_parent@example.com"
        }
        serializer = StudentOnboardingSerializer(data=payload)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['dcyn_requires_lsa_support'], 0)

    def test_invalid_age_boundary_fails(self):
        """Verify age out of 3-18 range fails validation."""
        payload = {
            "student_name": "Toddler John",
            "age": 1,  # Invalid (< 3)
            "evaluation_score": 80.0,
            "parent_consent_given": True,
            "guardian_email": "parent@example.com"
        }
        serializer = StudentOnboardingSerializer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn('age', serializer.errors)

    def test_invalid_evaluation_score_fails(self):
        """Verify evaluation score > 100 fails validation."""
        payload = {
            "student_name": "John Doe",
            "age": 10,
            "evaluation_score": 150.0,  # Invalid (> 100)
            "parent_consent_given": True,
            "guardian_email": "parent@example.com"
        }
        serializer = StudentOnboardingSerializer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn('evaluation_score', serializer.errors)

    def test_api_ingest_endpoint(self):
        """Test API endpoint POST request."""
        payload = {
            "student_name": "Sarah Connor",
            "age": 14,
            "evaluation_score": 62.0,
            "parent_consent_given": True,
            "guardian_email": "sarah@example.com"
        }
        response = self.client.post('/api/v1/student-onboarding/ingest/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['dcyn_is_eligible_for_program'], 1)
