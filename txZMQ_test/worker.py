# coding:utf-8
from txzmq import ZmqEndpoint, ZmqFactory, ZmqPubConnection, ZmqRouterConnection, ZmqREPConnection, ZmqDealerConnection
from twisted.internet import reactor
import uuid
from optparse import OptionParser
import json
import time
"""
cpu, the number of client, 
"""
"""
Example txzmq worker.

    python worker.py  --ep1=tcp://127.0.0.1:8880 --ep2=tcp://127.0.0.1:8881

    python worker.py  --ep1=tcp://127.0.0.1:10000 --ep2=tcp://127.0.0.1:10001
"""

def b2str(id):
    # print uuid.UUID(bytes=id)
    return str(uuid.UUID(bytes=id))

parser = OptionParser("")
parser.add_option("-p", "--ep1", dest="ep1", help="like tcp://127.0.0.1:8880")
parser.add_option("-e", "--ep2", dest="ep2", help="like tcp://127.0.0.1:8880")
parser.set_defaults(ep1="tcp://127.0.0.1:8880", ep2="tcp://127.0.0.1:8881")

(options, args) = parser.parse_args()

zf = ZmqFactory()

backend = ZmqEndpoint('bind', options.ep1)  # dealer
# frontend = ZmqEndpoint('bind', 'tcp://127.0.0.1:8881')    # router
pub = ZmqEndpoint('bind', options.ep2)

recv = ZmqREPConnection(zf, backend)  # REP
send = ZmqPubConnection(zf, pub)      # Pub
num = 0

# ZmqREPConnection


def doPrint(messageId, message):  # uuid
        # print('interval: ' ,time.time()-message[1])
        data = json.loads(message)
        print(type(data))
        print "Replying to %s, %r client-%s" % (b2str(messageId), data['time'], data['channel'])
        recv.reply(messageId, "%s %r " % (b2str(messageId), len(json.loads(message))/1024.0/1024.0))  # reply to client (id+msg) by mId
        global num
        num += 1
        print('the num of reply: %s' % num)
        send.publish(message, tag='btc')

recv.gotMessage = doPrint
reactor.run()







