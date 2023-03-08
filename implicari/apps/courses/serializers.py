from datetime import date

from rest_framework import serializers

from implicari.apps.events.models import Event
from implicari.apps.posts.models import Post

from .models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'


class PostCourseRetriveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'


class EventCourseRetriveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'


class CourseRetriveSerializer(serializers.ModelSerializer):

    next_event = serializers.SerializerMethodField()
    last_post = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'
        depth = 1

    def get_next_event(self, obj):
        today = date.today()
        event = obj.events.filter(date__gte=today).first()
        data = EventCourseRetriveSerializer(event, many=False).data

        return data

    def get_last_post(self, obj):
        post = obj.posts.last()
        data = PostCourseRetriveSerializer(post, many=False).data

        return data
