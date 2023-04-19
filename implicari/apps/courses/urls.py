from django.urls import path

from .views import CourseCreate, CourseParentList, CourseRetrive
from .views import CourseTeacherList


urlpatterns = [
    path('courses/create/', CourseCreate.as_view()),
    path('courses/teacher/', CourseTeacherList.as_view()),
    path('courses/parent/', CourseParentList.as_view()),
    path('courses/<pk>/', CourseRetrive.as_view()),
]
