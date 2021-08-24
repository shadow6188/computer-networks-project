########################################################################################################################
# Class: Computer Networks
# Date: 02/03/2021
# Lab3: TCP Client Socket
# Goal: Learning Networking in Python with TCP sockets
# Student Name: Gerardo Ochoa
# Student ID: 918631875
# Student Github Username: shadow6188
# Instructions: Read each problem carefully, and implement them correctly.
########################################################################################################################

# don't modify this imports.
import socket
import pickle

from client_helper import ClientHelper
import argparse

######################################## Client Socket ################################################################
"""
Client class that provides functionality to create a client socket is provided. Implement all the methods but bind(..)
"""

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--ip', type=str, help="Ip of server you want to connect to")
parser.add_argument('-p', '--port', type=int, help="Port of server you want to connect to")
parser.add_argument('-n', '--name', type=str, help="name of client")
args = parser.parse_args()


class Client(object):

    def __init__(self):
        """
        Class constructor
        """
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.helper = None

    def connect(self, server_ip_address, server_port, name):
        """
        TODO: Create a connection from client to server
              Note that this method must handle any exceptions
        :server_ip_address: the know ip address of the server
        :server_port: the port of the server
        """
        try:
            self.client.connect((server_ip_address, server_port))
            connected = self.receive()
            print(f"Successfully connected to {server_ip_address}/{server_port}")
            self.client_helper(connected['client_id'], name)

        except socket.timeout:
            print("Server not found")

    def bind(self, client_ip='', client_port=12000):
        """
        DO NOT IMPLEMENT, ALREADY IMPLEMENTED
        This method is optional and only needed when the order or range of the ports bind is important
        if not called, the system will automatically bind this client to a random port.
        :client_ip: the client ip to bind, if left to '' then the client will bind to the local ip address of the machine
        :client_port: the client port to bind.
        """
        self.client.bind((client_ip, client_port))

    def send(self, data):
        """
        TODO: Serializes and then sends data to server
        :param data: the raw data to serialize (note that data can be in any format.... string, int, object....)
        :return: VOID
        """
        data_serialized = pickle.dumps(data)
        self.client.send(data_serialized)

    def receive(self, max_alloc_buffer=4096):
        """
        TODO: Deserializes the data received by the server
        :param max_alloc_buffer: Max allowed allocated memory for this data
        :return: the deserialized data.
        """

        raw_data = self.client.recv(max_alloc_buffer)
        if raw_data:
            deserialized_data = pickle.loads(raw_data)
            return deserialized_data
        else:
            return None

    def client_helper(self, id, name):
        """
        TODO: create an object of the client helper and start it.
        """
        self.helper = ClientHelper(self, id, name)
        self.helper.start()

    def close(self):
        """
        TODO: close this client
        :return: VOID
        """
        self.client.close()


# main code to run client
if __name__ == '__main__':
    client = Client()
    if not args.ip:
        args.ip = input("Enter the server IP Address:")
    if not args.port:
        args.port = int(input("Enter the server port:"))
    if not args.name:
        args.name = input("Enter a username:")
    client.connect(args.ip, args.port, args.name)  # creates a connection with the server
