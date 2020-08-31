from rest_framework import viewsets
from .serializers import SessionSerializer, GameSerializer
from .models import Session, Game
from rest_framework import status
from rest_framework.response import Response
from django.db.models import F, Sum


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

        total_vibhu_points = Game.objects.aggregate(Sum('vibhu_score'))['vibhu_score__sum']
        total_dad_points = Game.objects.aggregate(Sum('dad_score'))['dad_score__sum']

        score['vibhu_session_wins'] = vibhu_session_wins
        score['dad_session_wins'] = dad_session_wins
        score['draw_session'] = draw_session
        score['vibhu_game_wins'] = vibhu_game_wins
        score['dad_game_wins'] = dad_game_wins
        score['total_vibhu_points'] = total_vibhu_points
        score['total_dad_points'] = total_dad_points

        return Response(score, status=status.HTTP_200_OK)

    def get_graph_data(self, request, *args, **kwargs):
        result = {}
        vibhu_games_graph = []
        dad_games_graph = []

        vibhu_points_graph =[]
        dad_points_graph =[]

        for session in Session.objects.all():
            #SESSION
            vibhu_games_won_by_session = Game.objects.filter(session=session, vibhu_score__gte=F('dad_score')).count()
            dad_games_won_by_session = Game.objects.filter(session=session, dad_score__gte=F('vibhu_score')).count()

            vibhu_games_graph.append([session.date, vibhu_games_won_by_session])
            dad_games_graph.append([session.date, dad_games_won_by_session])

            #GAMES
            vibhu_points_by_session = Game.objects.filter(session=session).aggregate(Sum('vibhu_score'))['vibhu_score__sum']
            dad_points_by_session = Game.objects.filter(session=session).aggregate(Sum('dad_score'))['dad_score__sum']

            vibhu_points_graph.append([session.date, vibhu_points_by_session])
            dad_points_graph.append([session.date, dad_points_by_session])

        result['vibhu_games_graph'] = vibhu_games_graph
        result['dad_games_graph'] = dad_games_graph

        result['vibhu_points_graph'] = vibhu_points_graph
        result['dad_points_graph'] = dad_points_graph

        return Response(result, status=status.HTTP_200_OK)
