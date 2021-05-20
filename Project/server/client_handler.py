########################################################################################################################
# Class: Computer Networks
# Date: 02/03/2020
# Lab3: Server support for multiple clients
# Goal: Learning Networking in Python with TCP sockets
# Student Name:Gerardo Ochoa
# Student ID: 918631975
# Student Github Username: shadow6188
# Lab Instructions: No partial credit will be given. Labs must be completed in class, and must be committed to your
#               personal repository by 9:45 pm.
# Running instructions: This program needs the server to run. The server creates an object of this class.
#
########################################################################################################################
import hashlib
import threading
import pickle
import datetime
import PGP
import bot

from menu import Menu


class Channel(object):
    def __init__(self, channel_id, admin, private, public, mod, bots):
        self.mod = mod
        self.public = public
        self.private = private
        self.id = channel_id
        self.admin = admin
        self.bot = bots


class ClientHandler:
    """
    The client handler class receives and process client requests
    and sends responses back to the client linked to this handler.
    """

    def __init__(self, server_instance, client_handler, addr):
        """
        Class constructor already implemented for you.
        :param server_instance: passed as 'self' when the object of this class is created in the server object
        :param client_handler: the accepted client on server side. this handler, by itself, can send and receive data
                             from/to the client that is linked to.
        :param addr: addr[0] = server ip address, addr[1] = client id assigned buy the server
        """
        self.server_ip = addr[0]
        self.client_id = addr[1]
        self.client_name = None
        self.menu = Menu()
        self.server = server_instance
        self.handler = client_handler
        self.messages = {}
        self.print_lock = threading.Lock()  # creates the print lock
        self.send_id(self.client_id)
        self.done = False
        self.channel = None
        self.bot = None
        self.routing = False
        self.distances = {}

    def process_requests(self):
        """
        :return: VOID
        """
        try:
            while True:
                if self.done:
                    break
                request = self.receive()
                self.process_request(request)
        except ConnectionResetError:
            self.log(f"connection reset by {self.client_name}")
        # except Exception as error:
        #    self.log(error)

    def process_request(self, request):
        """
        :request: the request received from the client. Note that this must be already deserialized
        :return: VOID
        """
        response = {}
        '''
        if self.routing:
            """best idea i could come up with is telling the client to do routing everytime there is a new
                client on the server, between request, hopefully its not noticeable
            """
            self.log(f"sending a routing request to {self.client_name}")

            users = {}

            for client in self.server.handlers:
                if client is not self:
                    print(f'handler {client.client_name} at ip {client.server_ip}')
                    users.update({client.client_name: client.server_ip})
            self.send({'ping': users})
            self.routing = False
        '''
        if 'name' in request:  # check for first request, which is meant to pass name to server from client
            self.save_name(request['name'])
            client_info = ["Your client info is:",
                           f"Client Name: {self.client_name}",
                           f"Client Id: {self.client_id}"]
            response.update({'print': client_info, 'acknowledge': 0})

        elif 'option' in request:
            option = self.menu.option(request['option'])
            response.update(self.menu.request_headers(self, option))

        elif 'menu' in request:  # if menu requested then send the menu
            self.log(f"menu sent to {self.client_name}")
            response.update({'print': self.menu.get()})
            response.update({'input': {'option': "Your option <enter a number>:"}})

        elif 'chat' in request:
            decrypted = PGP.decrypt_text(self.channel.private, self.channel.mod, request['chat'])

            if decrypted[0] == '#':
                special = decrypted.removeprefix('#')
                special = special.split(' ', 1)[0]

                if special == 'exit':
                    if self.client_name == self.channel.admin:
                        for client in self.server.handlers:
                            if client.channel == self.channel:  # sends exit signal to all clients in chat
                                client.send({'exit': None})

                elif special == 'bye':
                    if self.client_name != self.channel.admin:
                        self.send({'exit': None})  # sends the exit signal to client if not admin

                else:  # if not bye or exit assume its a private message( look for matching names)
                    self.send_message_to(decrypted, request['hash'], special)
            else:
                self.channel.bot.process_message(self, decrypted)  # check messages here
                self.send_message_everybody_else(decrypted, request['hash'], self.client_name)

        elif len(request) > 0:
            #  self.log("other options selected")
            headers = self.menu.response_headers(self, request)
            response.update(headers)

        else:
            self.log("something went wrong with the request")

        self.send(response)

        # delay formulae + ping

    def route_update(self):
        self.routing = True

    def channel_drop(self):
        message = "You have been dropped"
        self.send({'chat': PGP.encrypt_text(self.channel.private, self.channel.mod, message),
                   'hash': hashlib.sha1(message.encode()).hexdigest(), 'name': self.channel.bot.name,
                   'exit': 0})
        self.channel = None

    def send_message_to(self, message, hash, receiver):
        """message from this client to receiver"""
        for client in self.server.handlers:
            if client.client_name == receiver:
                sending = {'chat': PGP.encrypt_text(self.channel.private, self.channel.mod, message),
                           'hash': hash, 'name': self.client_name}
                client.send(sending)

    def send_message_everybody_else(self, message, hash, name):
        """message to everybody else on same channel"""
        for client in self.server.handlers:
            if client is not self:
                if client.channel == self.channel:
                    sending = {'chat': PGP.encrypt_text(self.channel.private, self.channel.mod, message),
                               'hash': hash, 'name': name}
                    client.send(sending)

    def save_name(self, name):
        self.client_name = name
        self.log(f'Client {self.client_id} name set to {self.client_name}')

    def get_users(self):  # correctly returning a list with client names with id
        handlers = ["users connected"]
        for handler in self.server.handlers:
            handlers.append(str(handler.client_name) + ':' + str(handler.client_id))
        return handlers

    def record_channel(self, channel_id, admin, private, public, mod):
        # saving channel existence in server
        self.channel = Channel(channel_id, admin, private, public, mod, self.bot)
        self.server.chats.append(self.channel)

    def create_bot(self, name):
        self.bot = bot.Bot(name, self.server)
        self.bot.create_token(self.client_id)

    def finalize_bot(self, permissions):
        self.bot.set_permissions(permissions)

    def join_channel(self, channel_id):
        for chat in self.server.chats:
            if chat.id == channel_id:
                print(f"{self.client_name} joining channel ", channel_id)
                self.channel = chat
                break

    def channel_members(self, channel_id):
        members = []
        for clients in self.server.handlers:
            if clients.channel.id == channel_id:
                members.append(clients.client_name)
        return members

    def save_message(self, message, recipient):
        # print(recipient)
        recipient = self.get_handler(int(recipient))

        if recipient is None:  # check for valid sender
            return 1
        else:
            self.pass_message(recipient, message, "Private")
            return 0

    def broadcast(self, message):
        for recipient in self.server.handlers:
            self.pass_message(recipient, message, "Broadcast")

    def pass_message(self, recipient, message, message_type):
        if self.client_name not in recipient.messages:
            recipient.messages.update({self.client_name: []})  # add messages to recipient list(create if necessary)
        arrived = datetime.datetime.now()
        recipient.messages[self.client_name].append((arrived.strftime('%d/%m/%y %I:%M %p'),
                                                     (message + f" ({message_type} message from {self.client_name})")))

    def get_messages(self):
        m = []
        # should be a better way to do this
        for each in self.messages.keys():
            for message in self.messages[each]:
                m.append(f'{message[0]}: {message[1]}')
        if not m:
            return ["No Messages"]
        else:
            self.messages.clear()
            return m

    def get_handler(self, id_num):

        for each in self.server.handlers:
            if each.client_id == id_num:
                return each
        # if not found
        return None

    def send(self, data):
        """
        """
        serialized = pickle.dumps(data)
        self.handler.send(serialized)

    def receive(self, max_mem_alloc=4096):
        """
        receive the data, deserializes the data received
        :max_mem_alloc: an integer representing the maximum allocation (in bytes) in memory allowed
                        for the data that is about to be received. By default is set to 4096 bytes
        :return: the deserialized data
        """
        data = self.handler.recv(max_mem_alloc)
        if data:
            deserialized_data = pickle.loads(data)
            return deserialized_data
        else:
            return None

    def send_id(self, client_id):
        """
        send the client id to the client
        """
        self.log(f'Client {client_id} connected')
        client_id = {'client_id': client_id}
        self.send(client_id)

    def log(self, message):
        """
        log a message on the server windows.
              note that before calling the print statement you must acquire a print lock
              the print lock must be released after the print statement.
        """
        self.print_lock.acquire()
        print(message)
        self.print_lock.release()

    def end(self):
        self.done = True
        self.server.handlers.remove(self)

    def run(self):
        """
        Already implemented for you
        """
        self.process_requests()
