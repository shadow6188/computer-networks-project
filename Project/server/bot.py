import hashlib

import PGP
import time


class Bot(object):
    def __init__(self, name, server):
        self.name = name
        self.permissions = None  # copy of text
        self.token = None
        self.ready = False
        # permissions
        self.welcome = False
        self.warning = False
        self.drop = False
        self.compute = False
        self.inactive = False

        self.inappropriate = ['fuck', 'shit']
        self.track = {}

        self.server = server

    def create_token(self, client_id):
        names = self.name + str(client_id)
        self.token = hashlib.sha1(names.encode()).hexdigest()

    def set_permissions(self, permissions):
        self.permissions = permissions

        for char in permissions:
            if char == '1':
                self.welcome = True
            elif char == '2':
                self.warning = True
            elif char == '3':
                self.drop = True
            elif char == '4':
                self.compute = True
            elif char == '5':
                self.inactive = True
        self.ready = True

    def return_config(self):
        configuration = [f"{self.name}'s Configuration:",
                         f"Token: {self.token}",
                         f"Permissions Enabled: {self.permissions}",
                         f"Status: {'ready' if self.ready else 'not ready'}"]
        return configuration

    def process_message(self, handler, message):

        if self.warning:
            """check text & use handler to send warning"""
            for each in self.inappropriate:
                if each in message:
                    print("inappropriate message")
                    if handler.client_name not in self.track:  # if not on record, create one
                        self.track.update({handler.client_name: 1})
                    else:  # else increment count of warnings
                        self.track.update({handler.client_name: self.track[handler.client_name] + 1})
                    message = f"warning you have sent an inappropriate message," \
                              f" you have {self.track[handler.client_name]} infractions"
                    handler.send({'chat': PGP.encrypt_text(handler.channel.private, handler.channel.mod, message),
                                  'hash': hashlib.sha1(message.encode()).hexdigest(), 'name': self.name})
                    break  # only one warning per message regardless of num words

        if self.drop:
            if handler.client_name in self.track:
                if self.track[handler.client_name] > 2:
                    """check warnings if 3+ drop from channel"""
                    handler.channel_drop()
        if self.compute:
            """ TODO: gotta figure out response time"""
            """check for compute signal and do stuff"""
            if message == "I am wondering what's the response time of this message":
                print("asked for compute")
                # rt =
                message = f'{handler.client_name}, the response time of your message is  ms'
                handler.send({'chat': PGP.encrypt_text(handler.channel.private, handler.channel.mod, message,),
                              'hash': hashlib.sha1(message.encode()).hexdigest(), 'name': self.name})

    def welcome_message(self, private, mod, name, handlers):
        time.sleep(.5)
        message = f'Welcome #{name}'
        encrypted = PGP.encrypt_text(private, mod, message)
        for client in handlers:
            if client.channel.bot == self:
                client.send({'chat': encrypted, 'hash': hashlib.sha1(message.encode()).hexdigest(), 'name': self.name})


def get_permissions():
    possible = ['The disabled permissions for this bot are:',
                '1. Welcome users right after they join a channel.',
                '2. Show a warning to the users when they send words that are not allowed',
                '3. Drop users from the channel after 3 warnings',
                '4. Compute the response time of a message when the user request it',
                '5. Inform the user when it has been inactive on the channel for more than 5 minutes.']
    return possible
