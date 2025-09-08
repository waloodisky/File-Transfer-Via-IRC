#change these variables
target = "#test"
server = "localhost"
nickname = "username2"
port = 6667

import sys
import base64
import irc.client

start=None
data=""
file=None
def on_connect(connection, event):
	if irc.client.is_channel(target):
		connection.join(target)
  

def on_msg(connection, event):
    message = event.arguments[0]
    global file
    global start
    global data
    if message.startswith("END:"):
    	start=False
    	decoded = base64.b64decode(data.encode("ascii"))
    	print(1)
    	with open(file, "wb") as f:
    		print(2)
    		f.write(decoded)
    if start and message.startswith("PART"):
    	data+= message[message.index(":")+1:]
    if message.startswith("START:"):
    	data=""
    	file=message[6:]
    	start=True

def on_disconnect(connection, event):
    raise SystemExit()


reactor = irc.client.Reactor()
try:
    c = reactor.server().connect(server, port, nickname)
except irc.client.ServerConnectionError:
    print(sys.exc_info()[1])
    raise SystemExit(1) from None
c.add_global_handler("welcome", on_connect)
c.add_global_handler("disconnect", on_disconnect)
c.add_global_handler("pubmsg", on_msg)
c.add_global_handler("privmsg", on_msg)
reactor.process_forever()