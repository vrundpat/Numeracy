import socket
import pickle


class Client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # The socket is created on instantiation

        # Typically the servr IP would be the server's IP but since the server and client on the same machine, this hould be fine
        # If server was running remotely, the line would become: self.server = "10.0.0.128" (THE server machine IP)
        self.server = socket.gethostbyname(socket.gethostname())
        self.port = 8080  # Port server is running on
        self.server_address = (self.server, self.port)  # Address Tuple
        try:
            self.socket.connect(self.server_address)  # connect to the server
        except socket.error:
            pass

    def send(self, data):
        """
        Send the data/message to the server and return the server's response
        :param data: Arbitrary
        :return: String
        """
        try:
            if data == "Accuracy":
                self.socket.send(pickle.dumps(data))  # Use pickle to convert the data into a pickled object and send it to the sever
                accuracy = self.socket.recv(2048).decode()  # Decode the server's response into 2048 bytes (padded/un-padded) and send the user
                return accuracy
            else:
                self.socket.send(pickle.dumps(data))
                prediction = self.socket.recv(2048).decode()
                return prediction
        except socket.error as e:
            print(e)
