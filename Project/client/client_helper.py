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
        request = {"payload": None}
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
        request = {}

        try:
            while True:
                response = self.client.receive()
                if not response:  # first check if
                    continue
                if 'print' in response:
                    # print works
                    for line in response['print']:
                        print(line)
                    print('\n')
                if 'input' in response:
                    # got input key processed properly
                    for key in response['input'].keys():
                        # thinking of sending type to check input client side
                        request[key] = input(response['input'][key])
                if 'acknowledge' in response:  # check if this is a response to request
                    self.send_request(self.create_request())
                    continue

                if request.keys():
                    self.send_request(request)
                    request.clear()

        except Exception as err:
            print("error is ", err)

    def start(self):
        """
        TODO: create a request with your student info using the self.request(....) method
              send the request to the server, and then process the response sent from the server.
        """
        self.send_request({'name': self.name})  # first request passing name to server
        self.process_response()
