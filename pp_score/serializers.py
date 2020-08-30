from rest_framework import serializers
from .models import Session, Game

class SessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Session
        fields = '__all__'

class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = '__all__'
