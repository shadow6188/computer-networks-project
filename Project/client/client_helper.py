class ClientHelper:

    def __init__(self, client, client_id, client_name):
        self.client = client
        self.id = client_id
        self.name = client_name
        self.student_name = 'Gerardo Ochoa'  # TODO: your name
        self.student_id = 918631875  # TODO: your student id
        self.github_username = 'shadow6188'  # TODO: your github username

    def create_request(self):
        """
        TODO: create request with a Python dictionary to save the parameters given in this function
              the keys of the dictionary should be 'student_name', 'github_username', and
              'sid'.
        :return: the request created
        """
        request = {'payload': None, 'headers': None}
        return request

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
        try:
            while True:
                response = self.client.receive()
                if not response:  # first check if
                    break
                print("got response")
                if 'acknowledge' in response and response['acknowledge'] == 0:  # check if its an acknowledgment
                    print("acknowledgement")
                if 'print' in response:
                    for line in response['print']:
                        print(line)

        except Exception as err:
            print("error is ", err)

    def start(self):
        """
        TODO: create a request with your student info using the self.request(....) method
              send the request to the server, and then process the response sent from the server.
        """
        self.send_request({'name': self.name})  # first request passing name to server
        print(f'Client ID is :{self.id}')
        self.send_request(self.create_request())
        self.process_response()
