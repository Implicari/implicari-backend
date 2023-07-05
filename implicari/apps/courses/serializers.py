from datetime import date

from rest_framework import serializers

from .models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'


class CourseCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = (
            'id',
            'teacher',
            'is_archived',
            'created_at',
            'updated_at',
        )


class CourseRetriveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'
        depth = 1


class CourseUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = (
            'id',
            'teacher',
            'created_at',
            'updated_at',
        )
