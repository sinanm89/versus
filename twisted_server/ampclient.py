from twisted.internet import reactor, defer
from twisted.internet.protocol import ClientCreator
from twisted.protocols import amp
from ampserver import Ready


def doMath():
    creator = ClientCreator(reactor, amp.AMP)
    readyDeferred = creator.connectTCP('127.0.0.1', 8123)

    def hazir(ampProto):
        print '-'*30
        print ampProto
        print '-'*20
        return ampProto.callRemote(Ready, IS_READY=True)
    readyDeferred.addCallback(hazir)

    def doner(result):
        import ipdb; ipdb.set_trace()
        print result
        reactor.stop()

    defer.DeferredList([readyDeferred]).addCallback(doner)


def main():
    doMath()
    reactor.run()

if __name__ == '__main__':
    main()

### OY VEY

#
#     import json
# from twisted.internet import reactor
# from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
# from twisted.internet.protocol import connectionDone, ReconnectingClientFactory
# from twisted.protocols import amp
# from twisted.protocols.basic import LineReceiver
#
# from twisted.protocols.basic import LineReceiver
#
#
# class Echo(LineReceiver):
#
#     def connectionMade(self):
#         self.name = self.ip_name()
#         print "====== CLIENT %s ======" % self.name
#         print "IVE MADE A CONNECTION"
#         send = json.dumps({"IS_READY":True, "_command":"Ready", "_ask":23})
#
#
#     def ip_name(self):
#         # IP:PORT
#         return str(self.transport.getHost().host) + ":" + str(self.transport.getHost().port)
#
#     def connectionLost(self, reason=connectionDone):
#         print 'IVE DESTROYED THE CONNECTION'
#
#     def dataReceived(self, data):
#         print '- RECEIVED DATA : %s - ' % data
#         # for data_received in data.splitlines():
#         #     try:
#         #         received = json.loads(data_received)
#         #     except Exception, e:
#         #         print "EXCEPTION"
#         #         import ipdb;ipdb.set_trace()
#         #     for key,value in received.iteritems():
#         #         if key == "PHASE_CHANGE":
#         #             if value == "READY_PLAYERS":
#                         # send = json.dumps({"IS_READY":"False"})
#                         # send = json.dumps({"IS_READY":True})
#         #                 print send
#         #                 # self.sendLine(send)
#         #
#         #                 reactor.callLater(2, self.sendLine, send)
# #
#
# class EchoClientFactory(ReconnectingClientFactory):
#     # protocol = amp.AMP
#     maxRetries = 3
#
#     def startedConnecting(self, connector):
#         print 'Started to connect.'
#     def buildProtocol(self, addr):
#         print 'Connected.'
#         self.resetDelay()
#         return Echo()
#
#     def clientConnectionLost(self, connector, reason):
#         print 'Lost connection.  Reason:', reason
#         ReconnectingClientFactory.clientConnectionLost(self, connector, reason)
#
#     def clientConnectionFailed(self, connector, reason):
#         print 'Connection failed. Reason:', reason
#         ReconnectingClientFactory.clientConnectionFailed(self, connector,
#                                                          reason)
#
# # def main():
# #     factory = EchoClientFactory()
# #     reactor.connectTCP('127.0.0.1', 8123, factory)
# #     reactor.run()
# #
# # if __name__ == '__main__':
# #     main()
#
# from twisted.internet import reactor, defer
# from twisted.internet.protocol import ClientCreator
# from twisted.protocols import amp
# from ampserver import Ready
#
#
#
# def doMath():
#     creator = ClientCreator(reactor, amp.AMP)
#     deferred_user1 = creator.connectTCP('127.0.0.1', 8123)
#
#     def callback1(RECEIVED):
#         print 'IN CALLBACK'
#         print RECEIVED
#
#     def ready(ampProto):
#         print '-'*30
#         # import ipdb; ipdb.set_trace()
#         # ampProto.transport.write('{"IS_READY":True, "_command":"READY" }')
#         ampProto.callRemote(Ready, IS_READY=True)
#         print 'Called'
#         defer.DeferredList([deferred_user1]).addCallback(callback1)
#
#     deferred_user1.addCallback(ready)
#
#
#     # defer.DeferredList([deferred_user1]).addCallback(callback1)
#     #
#     # deferred_user1.addCallback(callback1)
#     # deferred_user2.addCallback(callback1)
#     # defer.DeferredList([deferred_user2]).addCallback(callback1)
#     # reactor.stop()
#
#     # divideDeferred = creator.connectTCP('127.0.0.1', 1234)
#
#     # def connected(ampProto):
#     #     return ampProto.callRemote(Divide, numerator=1234, denominator=2)
#
#     # divideDeferred.addCallback(connected)
#
#     # def trapZero(result):
#     #     result.trap(ZeroDivisionError)
#     #     print "Divided by zero: returning INF"
#     #     return 1e1000
#
#     # divideDeferred.addErrback(trapZero)
#
#     # defer.DeferredList([sumDeferred, divideDeferred]).addCallback(done)
#
# def main():
#     doMath()
#     reactor.run()
#
#
# if __name__ == '__main__':
#     main()