from rest_framework import viewsets
from .serializers import SessionSerializer, GameSerializer
from .models import Session, Game
from rest_framework import status
from rest_framework.response import Response
from django.db.models import F, Sum
from django.forms.models import model_to_dict


class SessionViewset(viewsets.ModelViewSet):
    serializer_class = SessionSerializer
    http_method_names = ['get','post']

    def get_queryset(self, request, *args, **kwargs):
        return Session.objects.all()

    def create(self, request, *args, **kwargs):
        key = self.request.GET.get('apiKey','')

        if key == 'vibz1!':
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({"not":"allowed"}, status=status.HTTP_401_UNAUTHORIZED)


class GameViewset(viewsets.ModelViewSet):
    serializer_class = GameSerializer
    http_method_names = ['get','post']

    def get_queryset(self):
        return Game.objects.all()

    def create(self, request, *args, **kwargs):
        key = self.request.GET.get('apiKey','')

        if key == 'vibz1!':
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({"not":"allowed"}, status=status.HTTP_401_UNAUTHORIZED)
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

class ScoreInputViewSet(viewsets.ViewSet):

    def get_current_session(self, request, *args, **kwargs):
        current_sesion = Session.objects.last()
        vibhu_games_won_by_session = Game.objects.filter(session=current_sesion, vibhu_score__gte=F('dad_score')).count()
        dad_games_won_by_session = Game.objects.filter(session=current_sesion, dad_score__gte=F('vibhu_score')).count()

        data = {}

        data['current_session_date'] = current_sesion.date
        data['current_session_id'] = current_sesion.id
        data['vibhu_score'] = vibhu_games_won_by_session
        data['dad_score'] = dad_games_won_by_session

        return Response(data, status=status.HTTP_200_OK)
