from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Parent, Student


User = get_user_model()


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = (
            'id',
            'course',
            'user',
        )


class _UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
        )
        model = User


class ParentSerializer(serializers.ModelSerializer):

    user = _UserSerializer(read_only=True)

    class Meta:
        model = Parent
        fields = '__all__'
        read_only_fields = (
            'id',
            'user',
        )
