import json
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import exceptions


class Chat(LineReceiver):

    def __init__(self, users):
        self.name = None
        self.users = users
        self.is_ready = False
        self.max_players = 2
        self.state = "WAIT_PLAYERS"

    def __unicode__(self):
        return "%s's Chat instance " % self.name

    def connectionMade(self):
        print 'Our current capacity is %s/%s' %(str(len(self.users)+1), self.max_players)
        self.handle_GETNAME()
        self.check_phase()

    def connectionLost(self, reason):
        if self.name in self.users:
            del self.users[self.name]

    def lineReceived(self, line):
        # import ipdb;ipdb.set_trace()
        try:
            data = json.loads(line)
            print data
        except exceptions.ValueError:
            data = None
            #TODO: logger here
        if data:
            print 'we have data, we need logic here'
            if self.state == "READY_PLAYERS":
                self.is_ready = data.get('is_ready', False)
            self.check_phase()
            #TODO: Parse json data to logic
            # self.broadcast_fphase_change(line)

    def handle_GETNAME(self):
        self.name = len(self.users)+1
        self.users[str(self.name)] = self
        self.sendLine("joined")

    def check_phase(self):
        if self.state == "WAIT_PLAYERS":
            self.current_player_count = len(self.users)
            if self.current_player_count == self.max_players:
                self.broadcast_phase_change("READY_PLAYERS")
        elif self.state == "READY_PLAYERS":
            if self.users_are_ready():
                self.broadcast_phase_change("START_GAME")
            else:
                #TODO: AT THIS POINT THE READY BUTTON FLASHES IN GAME
                pass
        elif self.state == "START_GAME":
            pass
        elif self.state == "INGAME":
            pass
        elif self.state == "ENDGAME":
            pass
        else:
            pass


    def broadcast_phase_change(self, phase):
        self.state = phase
        for users, protocol in self.users.iteritems():
            protocol.sendLine('{ "PHASE_CHANGE" : "%s" }' % phase)

    def users_are_ready(self):
        for user, protocol in self.users.iteritems():
            if not protocol.is_ready:
                return False
        return True


class ChatFactory(Factory):

    def __init__(self):
        self.users = {} # maps user names to Chat instances

    def buildProtocol(self, addr):
        return Chat(self.users)


reactor.listenTCP(8123, ChatFactory())
reactor.run()
