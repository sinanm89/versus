import json
import exceptions
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver


class VersusGame(LineReceiver):

    def __init__(self, users):
        self.name = None
        self.users = users
        self.is_ready = False
        self.max_players = 1
        self.state = "WAIT_PLAYERS"

    def __unicode__(self):
        return "%s's Connection instance " % self.name

    def connectionMade(self):
        print 'Our current capacity is %s/%s' % (str(len(self.users)+1), self.max_players)
        self.get_connection_name()
        self.check_phase()

    def get_connection_name(self):
        user_ip_port = self.transport.getHost()
        self.name = str(user_ip_port.host) + ":" + str(user_ip_port.port)
        self.users[str(self.name)] = self
        print "joined user ====="

    def lineReceived(self, line):
        try:
            data = json.loads(line)
            print "===== DATA RECEIVED IS : %s " % data
        except exceptions.ValueError:
            data = None
            #TODO: logger here
        if data:
            print 'we have data, we need logic here'
            if self.state == "READY_PLAYERS":
                self.is_ready = data.get('IS_READY', False)
            self.check_phase()
            if self.state == "START_GAME":
                print 'game started'
                pass

            #TODO: Parse json data to logic
        else:
            #TODO: send error message?
            pass

    def check_phase(self):
        if self.state == "WAIT_PLAYERS":
            self.current_player_count = len(self.users)
            if self.current_player_count == self.max_players:
                self.broadcast_phase_change("READY_PLAYERS")
        elif self.state == "READY_PLAYERS":
            if self.users_are_ready():
                self.broadcast_phase_change("START_GAME")
            else:
                print '===== USERS ARENT READY'
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
            send = { "PHASE_CHANGE" : phase }
            if self.state == "START_GAME":
                import ipdb; ipdb.set_trace()
                send['users'] = [key for key,value in self.transport.server.factory.users.iteritems()]
            protocol.sendLine(json.dumps(send))

    def users_are_ready(self):
        for user, protocol in self.users.iteritems():
            if not protocol.is_ready:
                return False
        return True

    def connectionLost(self, reason):
        print '- Connection lost.'
        if self.name in self.users:
            del self.users[self.name]

class VersusGameFactory(Factory):

    def __init__(self):
        self.users = {} # maps user names to Chat instances

    def buildProtocol(self, addr):
        return VersusGame(self.users)


reactor.listenTCP(8123, VersusGameFactory())
reactor.run()
