from twisted.protocols import amp


# class Divide(amp.Command):
#     arguments = [('numerator', amp.Integer()),
#                  ('denominator', amp.Integer())]
#     response = [('result', amp.Float())]
#     errors = {ZeroDivisionError: 'ZERO_DIVISION'}

class Ready(amp.Command):
    arguments = [('IS_READY', amp.Boolean())]
    response = [('RECEIVED', amp.Boolean()),
                 ('ceronimo', amp.String())]

    errors = {TypeError: '- TYPE ERR'}

class Math(amp.AMP):

    def connectionMade(self):
        print 'CONNECTION MADE'

    def ready(self, IS_READY):
        print '-'*30
        if IS_READY:
            print 'he is ready'
        elif not IS_READY:
            print 'HE AINT READY BRUH'

        return {'RECEIVED': True, 'ceronimo': 'hello'}
    Ready.responder(ready)


def main():
    from twisted.internet import reactor
    from twisted.internet.protocol import Factory

    pf = Factory()
    pf.protocol = Math
    reactor.listenTCP(1234, pf)
    print 'started'
    reactor.run()


if __name__ == '__main__':
    main()