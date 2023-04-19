from rest_framework import serializers

from .models import Event


class EventListSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'id',
            'creator',
            'name',
            'date',
            'time',
        )
        model = Event


class EventDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = (
            'id',
            'creator',
            'course',
            'name',
            'description',
            'date',
            'time',
            'creation_timestamp',
            'update_timestamp',
        )
        model = Event


class EventCreateSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'name',
            'description',
            'date',
            'time',
        )
        model = Event


class EventUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'name',
            'description',
            'date',
            'time',
        )
        model = Event


class EventCancelSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'canceled',
        )
        model = Event