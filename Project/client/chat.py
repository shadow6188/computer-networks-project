import readline
import sys


class Chat(object):
    def __init__(self, server, channel_id, publicKey, creator):
        self.creator = creator
        self.id = channel_id
        self.server = server
        self.key = publicKey

    def chat_start(self):
        print(f"Private key received from server and channel {self.id} was successfully created!\n")

        """TODO: start listening thread here"""

        print(f'----------------------- Channel {self.id} ------------------------\n')
        print("All the data in this channel is encrypted")

        print('General Admin Guidelines:')
        print(f'1. #{self.creator} is the admin of this channel')
        print("2. Type '#exit' to terminate the channel (only for admins)\n")

        print('General Chat Guidelines:')
        print('1. Type #bye to exit from this channel. (only for non-admins users)')
        print('2. Use #<username> to send a private message to that user.\n')

        print("Waiting for other users to join....\n")

    def chat_listen(self):
        while True:
            response = self.server.receive()
            if not response:
                continue
            """do stuff here"""
            if 'chat' in response:
                copy = readline.get_line_buffer()
                print('\u001B[2K\r', end='')
                print(response['chat'])
                print(">", end='', flush=True)
                print(copy, end='', flush=True)
            elif "exit" in response:
                break
