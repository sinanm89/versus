import json
import random
from twisted.internet.protocol import Factory
from twisted.protocols import amp
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import exceptions

class Hello(amp.Command):
    arguments = [('text', amp.String())]
    response =  [('result', amp.String())]

class Ready(amp.Command):
    arguments = [('IS_READY', amp.Boolean())]
    response =  [('check', amp.String())]

class PhaseChange(amp.Command):
    arguments = [('phase', amp.String(optional=True))]
    response = [('PHASE_CHANGE', amp.String())]


class VersusGameConnection(amp.AMP):

    def __init__(self, users):
        # super(VersusGameConnection, self).__init__()
        self.name = None
        self.users = users
        self.is_ready = False
        self.players_ready = []
        self.max_players = 2
        self.state = "WAIT_PLAYERS"

    def __unicode__(self):
        return "%s's Connection instance " % self.name

    def connectionMade(self):
        self.name = self.ip_name()
        self.users[str(self.name)] = self
        print "====== Connection To %s ======" % self.name
        print 'Our current capacity is %s/%s' % (str(len(self.users)), self.max_players)
        self.check_phase()

    def check_phase(self):
        print "- USERS ARE : ", self.users
        if self.state == "WAIT_PLAYERS":
            self.current_player_count = len(self.users)
            if self.current_player_count == self.max_players:
                print '- calling remote'
                import ipdb; ipdb.set_trace()
                # self.users
        elif self.state == "READY_PLAYERS":
            if self.users_are_ready():
                self.broadcast_phase_change("START_GAME")
            else:
                #TODO: AT THIS POINT THE READY BUTTON FLASHES IN GAME
                pass
            self.check_phase()
        elif self.state == "START_GAME":
            self.the_game = VersusGame(self.users)
            self.broadcast_phase_change("INGAME")
        elif self.state == "INGAME":
            print '- WE ARE IN GAME'
            pass
        elif self.state == "ENDGAME":
            pass
        else:
            pass

    def ip_name(self):
        return str(self.transport.getPeer().host) + ":" + str(self.transport.getPeer().port)

    @Hello.responder
    def hello(self, text):
        print '-- in hello'
        return {'result': text}

    @Ready.responder
    def ready(self, IS_READY):
        print '-- IN READY'
        if IS_READY:
            #broadcast this user is ready
            print "%s is ready" % self.name
            self.is_ready = IS_READY
            self.players_ready = self.transport.server.factory.players_ready
            self.transport.server.factory.players_ready[self.name] = self.is_ready
            #TODO:             SKETCHY
            # self.check_phase()
            return {'check':'doodle'}

    @PhaseChange.responder
    def phase_change(self, phase):
        self.state = phase
        print "- GAME PHASE CHANGED TO %s -" % phase
        # for user, protocol in self.users.iteritems():
            # user.callRemote(PhaseChange, phase="READY_PLAYERS")

        return {'PHASE_CHANGE': phase}
            # self.send_to_my_user()
    # PhaseChange.responder(phase_change)

    def send_to_my_user(self, data):
        return data

    def lineReceived(self, line):
        print '- line received: %s -' % line
        try:
            data = json.loads(line)
        except exceptions.ValueError:
            data = None
            #TODO: logger here
        if not data:
            pass
        else:
            if self.state == "READY_PLAYERS":
                print '-'*30
                self.is_ready = data.get("IS_READY", False)
                self.players_ready = self.transport.server.factory.players_ready
                self.transport.server.factory.players_ready[self.name] = self.is_ready
                self.check_phase()

            elif self.state == "START_GAME":
                # Check to see if everyone got to ingame
                # init game
                print '- All Players Ready, begin game -'
                self.broadcast_phase_change("INGAME")

            elif self.state == "INGAME":
                # Game loops
                print '- INGAME -'
                #if data is 'emote' then do emote
                self.the_game.blame(data)

            elif self.state == "ENDGAME":
                pass
            else:
                #TODO: send error message?
                pass


    def broadcast_phase_change(self, phase):
        self.state = phase
        print "- GAME PHASE CHANGED TO %s -" % phase
        for users, protocol in self.users.iteritems():
            # import ipdb; ipdb.set_trace()
            # PhaseChange.responder(users.phase_change(phase))
            pass
            # protocol.sendLine('{ "PHASE_CHANGE" : "%s" }' % phase)

    def broadcast_my_action(self, action):
        for user, protocol in self.users.iteritems():
            if protocol != self:
                self.sendLine()

    def users_are_ready(self):
        for user, ready in self.players_ready.iteritems():
            if not ready or ready == "False":
                print '%s IS NOT READY' % user
                return False
        print "- PLAYERS READY ARE :", self.transport.server.factory.players_ready
        return True

    def connectionLost(self, reason):
        # names should be strings always
        print "- Connection lost "
        self.broadcast_phase_change("WAIT_PLAYERS")
        if str(self.name) in self.users:
            self.transport.server.factory.update_users(self)


class VersusGameFactory(Factory):

    def __init__(self):
        self.users = {} # maps user names to Chat instances
        self.players_ready = {}

    def buildProtocol(self, addr):
        return VersusGameConnection(self.users)

    def update_users(self, user):
        del self.users[user.name]

class VersusGame(object):

    round = 0
    innocents = []
    guilty_ones = []
    accused_ones = {}

    def __init__(self, players):
        self.player_count = len(players)
        if self.player_count < 5:
            guilty_number = 1
        else:
            guilty_number = 2
        guilty_ones = random.sample(players, guilty_number)
        self.innocents = list(set(players)-set(guilty_ones))

    def end_round(self):
        pass

    def blame(self, data):
        data_type = data.get('accuse', None)
        for accuser, accused in data_type.iteritems():
            person_on_trial = self.accused_ones.get(accused)
            if not person_on_trial:
                self.accused_ones[accused] = [accuser]
            else:
                person_on_trial.append(accuser)

        self.blame_roster = '11'


def main():
    reactor.listenTCP(8123, VersusGameFactory())
    reactor.run()

if __name__ == '__main__':
    main()
