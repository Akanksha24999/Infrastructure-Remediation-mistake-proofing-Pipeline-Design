from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import StudentOnboarding
from .serializers import StudentOnboardingSerializer

class StudentOnboardingIngestView(APIView):
    """
    API Endpoint for ingesting raw student onboarding JSON payloads.
    Executes DCYN validation and returns processed binary flags.
    """

    def get(self, request):
        """Returns list of all onboarded student records."""
        students = StudentOnboarding.objects.all().order_by('-created_at')
        serializer = StudentOnboardingSerializer(students, many=True)
        return Response({
            "count": len(serializer.data),
            "results": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        """Ingests raw JSON payload, runs DCYN serializer, and saves record."""
        serializer = StudentOnboardingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Student onboarding payload validated and DCYN binary flags generated.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
