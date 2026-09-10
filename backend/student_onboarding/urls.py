from django.urls import path
from .views import StudentOnboardingIngestView

urlpatterns = [
    path('ingest/', StudentOnboardingIngestView.as_view(), name='student-onboarding-ingest'),
]
