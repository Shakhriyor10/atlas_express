# app/serializers.py
from rest_framework import serializers
from .models import BroadcastMessage

class BroadcastMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BroadcastMessage
        fields = ["id", "description", "image1", "image2", "image3", "created_at"]
