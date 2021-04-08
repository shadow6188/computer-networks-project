import threading
from threading import Thread

from udp_tracker import Tracker


def check_address(address):
    if len(address.split(":")) == 2:
        values = address.split(":")
    else:
        return False

    first = values[0]
    second = values[1]
    # print(f'ip is {first} and port is {second}')
    if not len(first.split(".")) == 4:
        return False  # check far ip by checking for 3 .
    try:
        second = int(second)  # make sure second part is an int
    except ValueError:
        return False

    return first, second


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
                if not response:  # first check if
                    continue
                if 'print' in response:
                    for line in response['print']:
                        self.log(line)
                    self.log('\n')
                if 'input' in response:
                    for key in response['input'].keys():
                        # thinking of sending type to check input client side
                        request[key] = self.read(response['input'][key])
                if 'UDP' in response:
                    # print("UDP chosen")
                    if not self.udp:  # if udp socket not setup then it will be
                        """ TODO: need to add check for proper values """
                        ip = self.read("Enter the address to bind your UDP client (e.g 127.0.0.1:6000): ")
                        address = check_address(ip)  # convert address to str int tuple
                        while not address:  # check for valid format
                            self.log(f"{ip} is an invalid address")
                            ip = self.read("Enter the address to bind your UDP client (e.g 127.0.0.1:6000): ")
                            address = check_address(ip)
                        self.udp = Tracker(self, address)
                        Thread(target=self.udp.listen).start()

                    recipient_ip = self.read("Enter the recipient address (e.g 127.0.0.1:6001) : ")

                    send = check_address(recipient_ip)  # convert address to str int tuple
                    while not send:
                        self.log(f"{recipient_ip} is an invalid address")
                        recipient_ip = self.read("Enter the address to bind your UDP client (e.g 127.0.0.1:6000): ")
                        send = check_address(recipient_ip)

                    message = self.read("Enter the message: ")
                    self.udp.send(bytes(message, 'utf-8'), send)

                    self.log(f"message sent to udp address: {recipient_ip}")

                if 'acknowledge' in response:  # check if this is a response to request
                    self.send_request(self.create_request())  # after finish sending message request menu again

                if 'exit' in response:
                    break
                if request.keys():
                    self.send_request(request)
                    request.clear()

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
