from rest_framework import serializers

from .models import Message


class MessageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        depth = 1
        fields = (
            'id',
            'sender',
            'subject',
            'created_at',
        )


class MessageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        depth = 1
        fields = (
            'id',
            'sender',
            'subject',
            'body',
            'created_at',
        )


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            'id',
            'course',
            'sender',
            'subject',
            'body',
            'created_at',
        )
        read_only_fields = (
            'id',
            'course',
            'sender',
            'created_at',
        )