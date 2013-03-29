# coding: UTF-8

"""
A PartyChat JabberBot
"""

from twisted.application import service
from twisted.python import log
from twisted.words.protocols.jabber import jid
from twisted.words.xish import domish
from wokkel.client import XMPPClient
from wokkel.xmppim import AvailablePresence, MessageProtocol



# Configuration parameters
THIS_JID = jid.internJID('you@yourdomain.com')
ROOM_JID = jid.internJID('yourRoom@im.partych.at')
NICK = u''
SECRET = ''
LOG_TRAFFIC = True


class EchoBotProtocol(MessageProtocol):
    def connectionMade(self):
        log.msg('Connected!', system='EchoBot')

        # send initial presence
        self.send(AvailablePresence())

    def connectionLost(self, reason):
        log.msg('Disconnected!', system='EchoBot')

    def onMessage(self, msg):
        log.msg(msg['from'], system='EchoBot')
        if msg['type'] == 'chat' and hasattr(msg, 'body'):
            log.msg(str(msg.body), system='EchoBot')
            reply = domish.Element((None, 'message'))
            reply['to'] = ROOM_JID.full()
            reply['type'] = 'chat'
            reply.addElement('body', content='echo: ' + str(msg.body))
            self.send(reply)


# Set up the Twisted application

application = service.Application('MUC Client')

client = XMPPClient(THIS_JID, SECRET, host='talk.google.com', port=5222)
client.logTraffic = LOG_TRAFFIC

echoBot = EchoBotProtocol()
echoBot.setHandlerParent(client)

client.setServiceParent(application)
