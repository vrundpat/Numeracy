import socket
from _thread import *
from threading import Thread
from NeuralNetwork import NeuralNetwork
import mnist
import keras
import pickle
import numpy as np


# IMPORTANT RESOURCES USED:
#   Socket Library:
#       - https://docs.python.org/3/library/socket.html
#
#  Serialization using Pickle:
#       - https://docs.python.org/3/library/pickle.html
#


def client_thread_for_persistence(connection):
    """
    Create a NeuralNetwork instance for this client on a new thread, and use a while loop to run infinitely to listen for messages on a different thread
    :param connection: Tuple
    :return: None
    """
    model = NeuralNetwork()  # Create the NeuralNetwork instance for this client
    model_thread = Thread(target=model_trainer_thread, args=(model,))  # Initialize a new thread for the Network to run and train on
    model_thread.start()  # Start the thread for the Network
    while True:  # This loop will run on the new thread created for this client and persist while listening for messages

        # Try Statements have to be used as the recv() function is a blocking function (execution in the loop will wait until the client sends a message)
        # and this message could be more than 2048 bytes, which would cause an error. In data larger than 2048 bytes is sent, thread will end.
        try:
            data = connection.recv(2048)  # Blocking function which will wait for messages limited to 2048 bytes as the data size required for this software is minimal
            data = pickle.loads(data)  # Load the pickled object into usable python

            if not data:  # If the data is null or pickle object was none or could not load properly, the client will be disconnected
                print("Disconnected: ", connection)
                print("Data: ", data)
                break

            #  2 DATA TYPES:
                # Need Accuracy: String
                # Predict: Numpy Array
            else:
                if data == "Accuracy":
                    accuracy = str(model.calculate_accuracy())  # Ge the accuracy of the NeuralNetwork instance associated with this client as a string
                    print("Received: ", data)
                    print("Sending : ", accuracy)
                    connection.sendall(str.encode(accuracy))  # sendall() will send ALL the encoded data to the client in this thread
                else:

                    # In the Predict Message:
                        # The data is converted into a Numpy Array, in case the data is not loaded properly
                        # The Numpy Array is Transposed since the GUI Layout is set up in a different orientation to allow user interaction
                    prediction = str(model.predict(np.array(data).T.reshape(1, 784)))
                    print("Received Matrix")
                    print("Sending: ", prediction)
                    connection.sendall(str.encode(prediction))  # Send the Prediction as a String
        except socket.error:
            break

    # Termination of loop means socket can't communiucate well with the client, so disconnect the client
    print("Disconnected Client {}".format(connection))
    connection.close()  # Safely close the connection for this client from the server


def model_trainer_thread(args):
    """
    This thread will be responsible for training the network
    :param args: NeuralNetwork
    :return: None
    """
    train_x = mnist.train_images() / 255  # Fetch the training image matrices divide by 255 to normalize the RBG values between 0 and 1
    train_x = train_x.reshape(train_x.shape[0], 784)  # Reshape these matrices into 1x784 matrices so the network model can take it in as a viable input
    train_y = mnist.train_labels()  # Fetch the training image labels
    train_y = keras.utils.to_categorical(train_y, 10)  # Convert the labels (eg. 5) to one-hot vectors ( [0, 0, 0, 0, 1, 0, 0, 0, 0] )
    args.train(train_x, train_y)  # Send in the training data to the network to train


def model_accuracy_thread(args):
    return args.calculate_accuracy()



#  SERVER IP
# server = "192.168.1.28"  # MUST CHANGE TO THE IPV4 OF THE MACHINE RUNNING THE SERVER
server = socket.gethostbyname(socket.gethostname())
port = 8080  # Run on port 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create the socket object with the given properties to stream data

#  Try statement must be used in case the server fails to create the socket, or bind to the port and given IP
try:
    server_socket.bind((server, port))  # Bind the server to the given port and IP
except socket.error as e:
    str(e)

# For performance purposes, this server only allows two users, change int=3 to allow more clients; this is purely done due to the
# lack of performance on the laptop
server_socket.listen(3)
print("Server Started")

# In this main thread, the sever will persist and listen for connections from clients; upon a connection, the server will start a new thread for the
# client
while True:
    connector, address = server_socket.accept()  # Blocking function accept() will halt execution until a client connects
    print("Connected to: ", address)
    start_new_thread(client_thread_for_persistence, (connector,))  # Upon connection, start a client thread for the client
