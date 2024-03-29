from django.db import IntegrityError
from rest_framework import serializers
from .models import Upvote


class UpvoteSerializer(serializers.ModelSerializer):
    
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Upvote
        fields = ['id', 'created_at', 'owner', 'post']

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                {'details': 'Your vote is already registered'}
            )
