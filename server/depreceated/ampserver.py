import json
from twisted.protocols import amp


# class Divide(amp.Command):
#     arguments = [('numerator', amp.Integer()),
#                  ('denominator', amp.Integer())]
#     response = [('result', amp.Float())]
#     errors = {ZeroDivisionError: 'ZERO_DIVISION'}

class Greetings(amp.Command):
    # arguments = []
    response = [('COMMANDS', amp.String())]

class Ready(amp.Command):
    arguments = [('IS_READY', amp.Boolean())]
    response = [('RECEIVED', amp.String()),]

    errors = {TypeError: '- TYPE ERR'}

class Falafel(amp.Command):
    arguments = [('a', amp.Boolean(optional=True))]
    response = [('b', amp.Boolean()),
                 ('c', amp.String(optional=True))]

    errors = {TypeError: '- TYPE ERR'}

class Math(amp.AMP):

    def connectionMade(self):
        print 'CONNECTION MADE'
        # self.callRemote(Greetings)

    @Greetings.responder
    def hello(self):
        return {'COMMANDS': "READY, falafel"}

    @Ready.responder
    def ready(self, IS_READY):
        print '-'*30
        if IS_READY:
            print 'he is ready'
        elif not IS_READY:
            print 'HE AINT READY BRUH'
        # self.germ = "no pls"
        # self.falafel()
        # self.remote(self.falafel())
        return {'RECEIVED': True}

    @Falafel.responder
    def falafel(self, a=None):
        print '- in falafel'

        return {"b": self.germ }

def main():
    from twisted.internet import reactor
    from twisted.internet.protocol import Factory

    pf = Factory()
    pf.protocol = Math
    reactor.listenTCP(8123, pf)
    print 'started'
    reactor.run()


if __name__ == '__main__':
    main()