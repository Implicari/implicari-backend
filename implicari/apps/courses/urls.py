from django.urls import path

from .views import CourseParentList, CourseRetrive
from .views import CourseTeacherList


urlpatterns = [
    path('courses/teacher/', CourseTeacherList.as_view()),
    path('courses/parent/', CourseParentList.as_view()),
    path('courses/<pk>/', CourseRetrive.as_view()),
]
