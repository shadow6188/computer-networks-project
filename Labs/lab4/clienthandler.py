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
import socket
import threading
import pickle


class ClientHandler:
    """
    The client handler class receives and process client requests
    and sends responses back to the client linked to this handler.
    """

    def __init__(self, server_instance, clienthandler, addr):
        """
        Class constructor already implemented for you.
        :param server_instance: passed as 'self' when the object of this class is created in the server object
        :param clientsocket: the accepted client on server side. this handler, by itself, can send and receive data
                             from/to the client that is linked to.
        :param addr: addr[0] = server ip address, addr[1] = client id assigned buy the server
        """
        self.server_ip = addr[0]
        self.client_id = addr[1]
        self.server = server_instance
        self.handler = clienthandler
        self.print_lock = threading.Lock()  # creates the print lock
        self.sendID(self.client_id)

    def process_requests(self):
        """
        TODO: Create a loop that keeps waiting for client requests.
              Note that the process_request(...) method is executed inside the loop
              Recall that you must break the loop when the request received is empty.
        :return: VOID
        """
        while True:
            raw = self.handler.recv(1024)
            if not raw:
                break
            request = pickle.loads(raw)
            self.process_request(request)

    def process_request(self, request):
        """
        TODO: This implementation is similar to the one you did in the method process_request(...)
              that was implemented in the server of lab 3.
              Note that in this case, the clienthandler is not passed as a parameter in the function
              because you have a private instance of it in the constructor that can be invoked from this method.
        :request: the request received from the client. Note that this must be already deserialized
        :return: VOID
        """

        self.log(f'Connected: Student {request["student_name"]}, Github Username:'
                 f' {request["github_username"]}, sid: {request["sid"]}')
        self.handler.send(pickle.dumps(1))

    def send(self, data):
        """
        TODO: serializes data with pickle, and then send the serialized data
        """
        serialized = pickle.dumps(data)
        self.handler.send(serialized)

    def receive(self, max_mem_alloc=4096):
        """
        TODO: receive the data, deserializes the data received
        :max_mem_alloc: an integer representing the maximum allocation (in bytes) in memory allowed
                        for the data that is about to be received. By default is set to 4096 bytes
        :return: the deserialized data
        """
        deserialized_data = pickle.loads(self.handler.recieve(max_mem_alloc))
        return deserialized_data

    def sendID(self, clientid):
        """
        TODO: send the client id to the client
        """
        client_id = {'clientid': clientid}
        serialized_data = pickle.dumps(client_id)
        self.handler.send(serialized_data)

    def log(self, message):
        """
        TODO: log a message on the server windows.
              note that before calling the print statement you must acquire a print lock
              the print lock must be released after the print statement.
        """
        self.print_lock.acquire()
        print(message)
        self.print_lock.release()

    def run(self):
        """
        Already implemented for you
        """
        self.process_requests()
