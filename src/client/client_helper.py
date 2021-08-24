import hashlib
import threading
from threading import Thread
from udp_tracker import Tracker
import chat
import client_helper_auxiliary as extra


class ClientHelper:

    def __init__(self, client, client_id, client_name):
        self.client = client
        self.id = client_id
        self.name = client_name
        self.student_name = 'Gerardo Ochoa'
        self.student_id = 918631875
        self.github_username = 'shadow6188'
        self.udp = None
        self.lock = threading.Lock()

    def create_request(self):
        """
        TODO: create request with a Python dictionary to save the parameters given in this function
              the keys of the dictionary should be 'student_name', 'github_username', and
              'sid'.
        :return: the request created
        """
        return {'menu': 1}

    def send_request(self, request):
        """
        TODO: send the request passed as a parameter
        :request: a request representing data deserialized data.
        """
        self.client.send(request)

    def process_response(self):
        """
        TODO: process a response from the server
              Note the response must be received and deserialized before being processed.
        :response: the serialized response.
        """
        """
        client expects instructions within a dictionary
        
        for example dictionary entry 'print' is supposed to have a list of strings to print
        
        entry has another dictionary in it with expected request headers as keys and prompt for a value as the value
        eg. {'option': "Your option <enter a number>:"}
        should result in request having an entry like this {'option': 1} 
        
        I am using acknowledge as a way to recognize the end an option so the client knows to request the menu again
        """
        request = {}

        try:
            while True:
                response = self.client.receive()
                if not response:
                    continue
                    '''
                if 'ping' in response:
                    routes = {}
                    users = response['ping']
                    for each in users.keys():
                        ping = self.ping.ping(users[each])
                        print(each, users[each], ping)

                    continue
                    '''
                if 'print' in response:
                    for line in response['print']:
                        self.log(line)
                    self.log('\n')
                if 'input' in response:
                    for key in response['input'].keys():
                        request[key] = self.read(response['input'][key])
                if 'UDP' in response:
                    # print("UDP chosen")
                    if not self.udp:  # if udp socket not setup then it will be
                        """ TODO: need to add check for proper values """
                        ip = self.read("Enter the address to bind your UDP client (e.g 127.0.0.1:6000): ")
                        addr = extra.ensure_address(self, ip)
                        self.udp = Tracker(self, addr)
                        Thread(target=self.udp.listen).start()
                        self.log(f'UDP client running and accepting other clients at udp address {addr[0]}:{addr[1]}')

                    recipient_ip = self.read("Enter the recipient address (e.g 127.0.0.1:6001) : ")

                    send = extra.ensure_address(self, recipient_ip)

                    message = self.read("Enter the message: ")
                    self.udp.send(message.encode(), send)

                    self.log(f"message sent to udp address: {recipient_ip}")
                if 'channel' in response:
                    """TODO: create chat"""
                    data = response['channel']
                    if 'member' in data:
                        channel = chat.Chat(self.client, data['id'], data['public'], data['mod'], data['creator'],
                                            self.name, data['member'])
                    else:
                        channel = chat.Chat(self.client, data['id'], data['public'], data['mod'], data['creator'],
                                            self.name)

                    channel.chat_start()
                    chat_listen = Thread(target=channel.chat_listen)

                    chat_listen.start()
                    """
                    The idea here is to continually request input and send that to the server,
                    meanwhile a separate thread will listen to messages from the server and print them out
                    when printing out, will get a copy of input buffer & store it. then use either '\r' or 
                    some ascii escape characters to clear the current line which should be user input.
                    print out the message, then move down to next line and print input buffer contents
                    """
                    while True:
                        if not chat_listen.is_alive():
                            break
                        message = input(f"{self.name}>")

                        if len(message) > 0:
                            hashed = hashlib.sha1(message.encode())
                            encrypted = extra.encrypt_text(channel.public, channel.mod, message)
                            self.send_request({'chat': encrypted, 'hash': hashed.hexdigest()})
                if 'acknowledge' in response:  # check if this is a response to request
                    request = self.create_request()  # after finish sending message request menu again
                if 'exit' in response:
                    print('closing client')
                    break
                if request.keys():
                    self.send_request(request)
                    request.clear()
                else:
                    print("nothing in request")
                    print(request.keys())
                    self.send_request(self.create_request())

        except Exception as err:
            print("error is ", err)

    def listen_udp(self):
        self.udp.listen()

    """Added lock to client so that udp messages would not be printed out during other print or input operations"""

    def log(self, string):
        self.lock.acquire()
        print(string)
        self.lock.release()

    def read(self, prompt):
        self.lock.acquire()
        response = input(prompt)
        self.lock.release()
        return response

    def start(self):
        """
        TODO: create a request with your student info using the self.request(....) method
              send the request to the server, and then process the response sent from the server.
        """
        self.send_request({'name': self.name})  # first request passing name to server
        self.process_response()
