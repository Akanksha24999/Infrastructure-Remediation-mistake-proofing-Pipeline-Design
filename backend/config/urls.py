from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/student-onboarding/', include('student_onboarding.urls')),
]
