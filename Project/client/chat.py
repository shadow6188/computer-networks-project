import hashlib
import readline

class Chat(object):
    def __init__(self, server, channel_id, public, mod, creator, name, members=None):
        self.creator = creator
        self.id = channel_id
        self.server = server
        self.public = public
        self.mod = mod
        self.members = members
        self.name = name

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

        if self.members:
            for each in self.members:
                print(each, end=' ')
                print('&', end=' ')
            print('\n')
            print("are already on the channel\n")
        else:
            print("Waiting for other users to join....\n")

    def chat_listen(self):
        while True:
            response = self.server.receive()
            if not response:
                continue
            """do stuff here"""

            if 'chat' in response:
                encrypted = response['chat']
                ehash = response['hash']
                message = decrypt_text(self.public, self.mod, encrypted)
                hash = hashlib.sha1(message.encode()).hexdigest()
                if ehash != hash:
                    continue  # drop if hashes don't match
                copy = readline.get_line_buffer()
                print('\u001B[2K\r', end='')  # clears current line
                print(response['name'], end='>')
                print(message)  # print out message
                print(f"{self.name}>", end='', flush=True)
                print(copy, end='', flush=True)  # print out input buffer contents
            if "exit" in response:
                print('\u001B[2K\r', end='')  # clears current line
                print('exiting chat')
                break

def PrivateKey(d, n, encrypted):  # applying private key AKA decryption
    return (encrypted ** d) % n


def decrypt_text(e, n, cipher):
    decrypt = [PrivateKey(e, n, each) for each in cipher]
    return ''.join([chr(each) for each in decrypt])
