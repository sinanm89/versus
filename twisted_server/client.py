import json
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.internet.protocol import connectionDone, ReconnectingClientFactory
from twisted.protocols.basic import LineReceiver

class Echo(LineReceiver):


    def connectionMade(self):
        self.name = self.ip_name()
        print "====== CLIENT %s ======" % self.name
        print "IVE MADE A CONNECTION"

    def ip_name(self):
        # IP:PORT
        return str(self.transport.getHost().host) + ":" + str(self.transport.getHost().port)

    def connectionLost(self, reason=connectionDone):
        print 'IVE DESTROYED THE CONNECTION'

    def dataReceived(self, data):
        print '- RECEIVED DATA : %s - ' % data
        for data_received in data.splitlines():
            try:
                received = json.loads(data_received)
            except Exception, e:
                print "EXCEPTION"
                import ipdb;ipdb.set_trace()
            for key,value in received.iteritems():
                if key == "PHASE_CHANGE":
                    if value == "READY_PLAYERS":
                        # send = json.dumps({"IS_READY":"False"})
                        send = json.dumps({"IS_READY":True})
                        print send
                        # self.sendLine(send)

                        reactor.callLater(2, self.sendLine, send)


class EchoClientFactory(ReconnectingClientFactory):

    maxRetries = 3

    def startedConnecting(self, connector):
        print 'Started to connect.'

    def buildProtocol(self, addr):
        print 'Connected.'
        self.resetDelay()
        return Echo()

    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.  Reason:', reason
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason
        ReconnectingClientFactory.clientConnectionFailed(self, connector,
                                                         reason)

def main():
    factory = EchoClientFactory()
    reactor.connectTCP('127.0.0.1', 8123, factory)
    reactor.run()

if __name__ == '__main__':
    main()

