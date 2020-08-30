from django.db import models

class Session(models.Model):

    VIBHU = 1
    DAD = 2
    DRAW = 3
    PLAYERS = [(VIBHU,'Vibhu'),
               (DAD, 'Dad'),
               (DRAW, 'Draw')]
    date = models.DateField(null=False, blank=False)
    notes = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(null=False, default=False)
    winner = models.IntegerField(choices=PLAYERS, default=DRAW)

class Game(models.Model):
    vibhu_score = models.IntegerField(null=False, blank=True, default=0)
    dad_score = models.IntegerField(null=False, blank=True, default=0)
    session = models.ForeignKey(Session, null=True, on_delete=models.SET_NULL, related_name='games')

    def save(self, *args, **kwargs):
        super(Game, self).save(*args, **kwargs)
        if self.session:
            vibhu_wins = 0
            dad_wins = 0
            for game in self.session.games.all():
                if game.vibhu_score > game.dad_score:
                    vibhu_wins += 1
                else:
                    dad_wins += 1
            if vibhu_wins > dad_wins:
                self.session.winner = Session.VIBHU
            elif vibhu_wins < dad_wins:
                self.session.winner = Session.DAD
            else:
                self.session.winner = Session.DRAW
            self.session.save()
