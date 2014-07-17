from twisted.internet import reactor, defer
from twisted.internet.protocol import ClientCreator
from twisted.protocols import amp
from ampserver import Ready


def doMath():
    creator = ClientCreator(reactor, amp.AMP)
    readyDeferred = creator.connectTCP('127.0.0.1', 1234)

    def hazir(ampProto):
        print '-'*30
        return ampProto.callRemote(Ready, IS_READY=True)
    readyDeferred.addCallback(hazir)

    def doner(result):
        print result
        reactor.stop()

        # reactor.stop()

    # divideDeferred = creator.connectTCP('127.0.0.1', 1234)
    #
    # def connected(ampProto):
    #     return ampProto.callRemote(Divide, numerator=1234, denominator=2)
    #
    # divideDeferred.addCallback(connected)
    #
    # def trapZero(result):
    #     result.trap(ZeroDivisionError)
    #     print "Divided by zero: returning INF"
    #     return 1e1000
    #
    # divideDeferred.addErrback(trapZero)
    #
    # defer.DeferredList([sumDeferred, divideDeferred]).addCallback(done)
    defer.DeferredList([readyDeferred]).addCallback(doner)

def main():
    doMath()
    reactor.run()


if __name__ == '__main__':
    main()