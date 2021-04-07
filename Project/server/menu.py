#######################################################################################
# File:             menu.py
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template Menu class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this Menu class, and use a version of yours instead.
# IMPORTANT:        This file can only resides on the server side.
# Usage :           menu = Menu() # creates object
#
########################################################################################
import client_handler
class Menu:
    """
    IMPORTANT MUST READ: The Menu class is the user interface that acts as a communication bridge between the user
    and the Client-Server architecture of this application. The Menu is always located on the Server side (machine running the server).
    However, it must be printed on the Client console by the ClientHelper object. In order to accomplish this, students
    must create a
    """

    @staticmethod
    def get():
        """
        TODO: shows the following menu on the client side
        ****** TCP/UDP Network ******
        ------------------------------------
        Options Available:
        1.  Get users list
        2.  Send a message
        3.  Get my messages
        4.  Send a direct message with UDP protocol
        5.  Broadcast a message with CDMA protocol
        6.  Create a secure channel to chat with your friends using PGP protocol
        7.  Join an existing channel
        8.  Create a Bot to manage a future channel
        9.  Get the Routing Table of this client with Link State Protocol
        10. Get the Routing Table of this network with Distance Vector Protocol
        11. Turn web proxy server on (extra-credit)
        12. Disconnect from server

        Your option <enter a number>:
        """
        # your code here
        options = ["1.  Get users list",
                   "2.  Send a message",
                   "3.  Get my messages",
                   "4.  Send a direct message with UDP protocol",
                   "5.  Broadcast a message with CDMA protocol",
                   "6.  Exit"]

        return options

    @staticmethod
    def option(option):
        """
        TODO: Ask the user to select an option from the menu
              Note. you must handle exceptions for options chosen that are not in the allowed range
        :return: an integer representing the option chosen by the user from the menu
        """
        try:
            option = int(option)
        except ValueError:  # option not an integer
            option = -1
        return option

    @staticmethod
    def request_headers(ClientHandler, option):
        """
        TODO: In this method students implement the headers of the menu. That's it, the options the server expect
              for each requests from the client related to this menu. For example, the headers for option 2,
              the expected headers in a client request are {'option':<integer>, 'message':<string>, 'recipient':<integer>}
        """
        if option == 1:
            ClientHandler.log("option 1 chosen by:" + ClientHandler.client_name)
            return {'print': ClientHandler.get_users(), 'acknowledge': 0}
        elif option == 2:
            ClientHandler.log("option 2 chosen by:" + ClientHandler.client_name)
            # no acknowledge here because this is not the end of the interaction
            return {'input': {'message': "Enter your message:", 'recipient id': "Enter recipient id:"}}
        elif option == 3:
            ClientHandler.log("option 3 chosen by:" + ClientHandler.client_name)
            return {'print': ClientHandler.get_messages(), 'acknowledge': 0}
        elif option == 4:
            ClientHandler.log("option 4 chosen by:" + ClientHandler.client_name)
            return {"UDP": 0, 'acknowledge': 0}
        elif option == 5:
            print("not implemented")
            return {}
        elif option == 6:
            ClientHandler.log(ClientHandler.client_name + " has disconnected")
            ClientHandler.end()
            return {'exit': 0}
        else:
            print(f'{option} is an invalid option')
            return {'acknowledge': 0}

    @staticmethod
    def response_headers(ClientHandler, request):
        """
        TODO: In this method students implement the headers of the menu. That's it, the options the server sends to
              the client for each response related to this menu. For example, the headers for the response of option 3
              are {'option':<integer>, 'messages':<Python Dictionary>}
        """

        if 'message' and 'recipient id' in request:  # processing second half of part 2 (storing message)

            ClientHandler.log(f"received message for {request['recipient id']}")

            if ClientHandler.save_message(request['message'], request['recipient id']):
                return {'print': ["failed to deliver message"]}
            else:  # message saved successfully
                return {'print': ['message sent'], 'acknowledge': 0}
