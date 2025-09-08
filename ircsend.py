#change these variables
file = "audio.mp3"
target = "#test"
server = "localhost"
nickname = "username1"
port = 6667

import sys
import base64
import irc.client

with open(file,"rb") as f:
	data=f.read()
encoded = base64.b64encode(data).decode("ascii")
message_length = 400
parts = [encoded[i:i+message_length] for i in range(0, len(encoded), message_length)]

def on_connect(connection, event):
	if irc.client.is_channel(target):
		connection.join(target)
	else:
		send(connection)

def on_join(connection, event):
	send(connection)
	

def send(connection):
	connection.privmsg(target, f"START:{file}")
	for i, part in enumerate(parts):
		connection.privmsg(target, f"PART{str(i+1)}:{part}")
	connection.privmsg(target, f"END:{file}")
	connection.quit("Using irc.client.py")


def on_disconnect(connection, event):
    raise SystemExit()


reactor = irc.client.Reactor()
try:
    c = reactor.server().connect(server, port, nickname)
except irc.client.ServerConnectionError:
    print(sys.exc_info()[1])
    raise SystemExit(1) from None
c.add_global_handler("welcome", on_connect)
c.add_global_handler("join", on_join)
c.add_global_handler("disconnect", on_disconnect)
reactor.process_forever()