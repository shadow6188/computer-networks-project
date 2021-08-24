
# TCP/UDP client-server network

A pair of programs that work together to create a client-server network through the use of the TCP & UDP protocols.

A server can be started by running the server script, and clients can be created by running the client script.
the network functions through the server providing any newly connected clients a menu which they can use to access the
services the server provides.

## How to use
1.First you must create a server by running the server.py script in the server folder, it will ask you to provide the ip address and port you wish to use.

2.Once you have a server running, then run the client script in the client folder. you will be ask to provide the ip and port of the server you wish to connect to as well as the username you want to use.

3.once you have successfully connected the server it will provide you with an id and a menu of the services which it provides.
## Services
I implemented 8 services in the server script

1.get user list

2.send of a message

3.get messages

4.send a direct message with UDP protocol

5.send broadcast message with cdma protocol

6.create secure chatroom

7.join a chatroom

8.create bot to manage future chatroom
