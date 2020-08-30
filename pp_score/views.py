from rest_framework import viewsets
from .serializers import SessionSerializer, GameSerializer
from .models import Session, Game
from rest_framework import status
from rest_framework.response import Response
from django.db.models import F


class SessionViewset(viewsets.ModelViewSet):
    serializer_class = SessionSerializer
    # filter_backends = [DjangoFilterBackend]
    # filter_fields = ['sell_date', 'buy_date']

    def get_queryset(self):
        return Session.objects.all()

class GameViewset(viewsets.ModelViewSet):
    serializer_class = GameSerializer
    # filter_backends = [DjangoFilterBackend]
    # filter_fields = ['sell_date', 'buy_date']

    def get_queryset(self):
        return Game.objects.all()

class ScoreViewset(viewsets.ViewSet):

    def get_score(self, request, *args, **kwargs):

        score = {}
        vibhu_session_wins = Session.objects.filter(winner=Session.VIBHU).count()
        dad_session_wins = Session.objects.filter(winner=Session.DAD).count()
        draw_session = Session.objects.filter(winner=Session.DRAW).count()

        vibhu_game_wins = Game.objects.filter(vibhu_score__gte=F('dad_score')).count()
        dad_game_wins = Game.objects.filter(dad_score__gte=F('vibhu_score')).count()


        score['vibhu_session_wins'] = vibhu_session_wins
        score['dad_session_wins'] = dad_session_wins
        score['draw_session'] = draw_session
        score['vibhu_game_wins'] = vibhu_game_wins
        score['dad_game_wins'] = dad_game_wins

        return Response(score, status=status.HTTP_200_OK)
