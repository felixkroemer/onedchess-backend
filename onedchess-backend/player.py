class Player():

    def __init__(self, dt):
        self._dt = dt
        self._sid = None
        self._partner = None
        self._game = None

    @property
    def dt(self):
        return self._dt

    @dt.setter
    def dt(self, dt):
        self._dt = dt

    @property
    def sid(self):
        return self._sid

    @sid.setter
    def sid(self, sid):
        self._sid = sid

    @property
    def partner(self):
        return self._partner

    @partner.setter
    def partner(self, partner):
        self._partner = partner

    @property
    def game(self):
        return self._game

    @game.setter
    def game(self, game):
        self._game = game
