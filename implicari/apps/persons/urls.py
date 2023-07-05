from django.urls import path

from .views import (
    ParentCreate,
    ParentList,
    StudentCreate,
    StudentList,
    StudentDetail,
    ParentDetail,
)


urlpatterns = [
    path('courses/<course_id>/students/', StudentList.as_view()),
    path('courses/<course_id>/students/create/', StudentCreate.as_view()),
    path('students/<pk>/', StudentDetail.as_view()),
    path('students/<student_id>/parents/', ParentList.as_view()),
    path('students/<student_id>/parents/create/', ParentCreate.as_view()),
    path('parents/<pk>/', ParentDetail.as_view()),
]