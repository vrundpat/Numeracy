import numpy as np
import mnist
import keras


# IMPORTANT RESOURCES USED:
#   Numoy Package:
#       - https://devdocs.io/numpy~1.14/
#
#   Keras and MNIST:
#       - https://keras.io/examples/mnist_dataset_api/
#
#   Activation functions:
#       - https://ml-cheatsheet.readthedocs.io/en/latest/activation_functions.html
#
#   Matrix Math:
#       - https://ml-cheatsheet.readthedocs.io/en/latest/linear_algebra.html


# noinspection PyAttributeOutsideInit,SpellCheckingInspection
class NeuralNetwork(object):
    def __init__(self):
        self.input = np.array((1, 784))
        self.output = np.array((1, 10))
        self.epochs = 0  # Number of iterations over the training data when training
        self.layers = [128, 128, 64, 10]  # Layers of this network; 3 Hidden and 1 Output Layers = 4 Layered Network
        self.wb = self.initialize_Weights_Biases()  # Initialize the weights and biases
        self.layer_outputs = {}  # Map to hold the outputs of each layer
        self.learning_rate = 0.5  # Learning rate; the magnitude of the "step" in a direction which reduces loss
        self.testX = (mnist.test_images() / 255).reshape(mnist.test_images().shape[0], 784)  # Testing Inputs
        self.testY = keras.utils.to_categorical(mnist.test_labels(), 10)  # Testing Outputs

    def initialize_Weights_Biases(self):
        """
        Create a map which will hold the biases and weights for each layer
        :return: Map[String, Numpy Array]
        """
        temp_map = {}
        for i in range(1, len(self.layers) + 1):
            if i == 1:
                temp_map["w" + str(i)] = np.random.randn(784, self.layers[i - 1])
                temp_map["b" + str(i)] = np.random.randn(1, self.layers[0])
            else:
                temp_map["w" + str(i)] = np.random.randn(self.layers[i - 2], self.layers[i - 1])
                temp_map["b" + str(i)] = np.random.randn(1, self.layers[i - 1])
        return temp_map

    @staticmethod
    def sigmoid_activation(n_array):
        """
        Apply the sigmoid function to the given numpy array
        :param n_array: Numpy Array
        :return: Numpy Array
        """
        return 1 / (1 + np.exp(-n_array))

    @staticmethod
    def softmax_activation(output_prediction):
        """
        Apply the softmax activation function to the output of the last layer, whose max index will be the network's prediction
        :param output_prediction: Numpy Array
        :return: Numpy Array
        """
        exps = np.exp(output_prediction - np.max(output_prediction, axis=1, keepdims=True))
        return exps / np.sum(exps, axis=1, keepdims=True)

    def feed_forward(self, generic_activation_function, output_activation_function):
        """
        Feed a given input through the network
        :param generic_activation_function: Sigmoid Function
        :param output_activation_function: Softmax Function
        :return: None
        """
        current = self.wb["w1"]  # Input to the next layer
        for i in range(1, len(self.layers) + 1):
            if i == 1: # Input Layer
                current = generic_activation_function(np.dot(self.input, current) + self.wb[
                    "b1"])  # Update current, so the output of one layer becomes input to another
                self.layer_outputs[str(i)] = current

            # Layers in between the input and output layers
            elif 1 < i <= len(self.layers) - 1:
                current = generic_activation_function(np.dot(current, self.wb["w" + str(i)]) + self.wb["b" + str(i)])
                self.layer_outputs[
                    str(i)] = current  # Store teh outputs of each layer so they can be used during backpropagation

            # On last iteration (last layer) instead of sigmoid, the softmax activation function is applied
            else:
                current = output_activation_function(np.dot(current, self.wb["w" + str(i)]) + self.wb["b" + str(i)])
                self.layer_outputs[str(i)] = current

    @staticmethod
    def sigmoid_prime(x):
        """
        Undo the sigmoid function using its derivative on a given Numpy Array
        :param x: Numpy Array
        :return: Numpy Array
        """
        return x * (1 - x)

    @staticmethod
    def calculate_error(prediction_from_network, actual_output):
        """
        Calculate the loss on the prediction of the network on a given input
        :param prediction_from_network: Numpy Array (the prediction made by the network when input was fed forward)
        :param actual_output: Numpy Array (one hot vector representing the actual output)
        :return: Numpy Array
        """
        error_vector = prediction_from_network - actual_output
        total_options = actual_output.shape[0]  # The 10 options for classification
        return error_vector / total_options

    def back_propagate(self, activation_derivative):
        """
        Adjust the weights and biases based on the calculated error of the output
        :param activation_derivative: Sigmoid Prime Function
        :return: None
        """
        # SOURCES USED FOR THIS FUNCTION:
        #    - https://www.youtube.com/watch?v=Ilg3gGewQ5U
        #    - https://www.youtube.com/watch?v=FaHHWdsIYQg
        #    - https://mlfromscratch.com/neural-networks-explained/#/
        #    - https://ml-cheatsheet.readthedocs.io/en/latest/backpropagation.html

        # PROCESS:
        #   - Calculate the change in the error with respect to change in each weight: dE / dW (Derivative of the error with respect to the weight)
        #       - dE/dW = dE/dA * dA/dO * dO/dW
        #           - Since the derviative can't be calcualted directly, partial derivaties are used
        #               - The cost if directly affected by the activagion in a given layer  (dE / aA)
        #               - The activation in a layer is directly affected by the inputs to that layer (dA / dO)
        #               - The inputs to a layer are directly affected by the weights associated wtih that layer (aO / aW)
        #       - Similarily: dE/dB = dE/aA * dA/dO * dO/dB
        #

        previous_layer_gradient = None # Holder variable which will hold the graident of a laye which will be used to calculate errors in aother layer
        for i in range(len(self.layers), 0, -1): # Iterate until all layers have had their corresponding weights adjusted
            if i == len(self.layers): # The output layer
                current_layer_delta = self.calculate_error(self.layer_outputs[str(i)], self.output)  # Error in output layer is the direct error in the network's prediction
                self.wb["w" + str(i)] -= self.learning_rate * np.dot(self.layer_outputs[str(i - 1)].T,current_layer_delta)

                # Since the bias will has a derivative of 1 (dO/aB = 1), it gets adjusted using the total sum of the error in a particular layer
                self.wb["b" + str(i)] -= self.learning_rate * np.sum(current_layer_delta)

                # The gradient of this layer is calculated using the errors in this layer and the weights of the current layer transposed as during
                # backpropagation, (Row x Col) becomes (Col x Row) to make sure the dimensions match up
                previous_layer_gradient = np.dot(current_layer_delta, self.wb["w" + str(i)].T)

            elif len(self.layers) - 1 >= i > 1: # Layers between the input and output layers

                # Since sigmoid does have a derivative, the error in these layers is directly proportional to the errors in the layers ahead, which is why
                # gradients of the next layer's are used when calculating the error matrix in this layer
                current_layer_delta = previous_layer_gradient * activation_derivative(self.layer_outputs[str(i)])
                self.wb["w" + str(i)] -= self.learning_rate * np.dot(self.layer_outputs[str(i - 1)].T, current_layer_delta)
                self.wb["b" + str(i)] -= self.learning_rate * np.sum(current_layer_delta)
                previous_layer_gradient = np.dot(current_layer_delta, self.wb["w" + str(i)].T)  # Calculate the gradient in this layer, so it can be used in another interation

            else:  # The input layer
                current_layer_delta = previous_layer_gradient * activation_derivative(self.layer_outputs[str(i)])

                # Input had to be re-shaped so it would have ideal dimensions for the dot product
                self.wb["w" + str(i)] -= self.learning_rate * np.dot(self.input.reshape(784, 1), current_layer_delta)
                self.wb["b" + str(i)] -= self.learning_rate * np.sum(current_layer_delta)

    def predict(self, data):
        """
        Given an input, feed the data through the network and make a prediction
        :param data: Numpy Array of size 1 by 784
        :return: Int
        """
        self.input = data
        self.feed_forward(self.sigmoid_activation, self.softmax_activation)
        return self.layer_outputs[
            str(len(self.layers))].argmax()  # Since softmax was used at the last layer, the index in that one-hot vector with the highest value will be the prediction made by the network

    def train(self, train_inputs, train_outputs):
        """
        Given the entire training set, train the network using recursion
        :param train_inputs: MNIST Train Images
        :param train_outputs: MINST Train Labels
        :return: None
        """
        if self.epochs == 5: return
        for i in range(len(train_inputs)):
            self.input = train_inputs[i]
            self.output = train_outputs[i]
            self.feed_forward(self.sigmoid_activation, self.softmax_activation)
            self.back_propagate(self.sigmoid_prime)

        # Shuffle the training set on each iteration so the network does not over-fit an order of data
        shuffledX, shuffledY = self.shuffle(train_inputs, train_outputs)
        self.epochs += 1
        self.train(shuffledX, shuffledY)  # Recursive call

    @staticmethod
    def shuffle(x, y):
        """
        Shuffle the given Numpy Arrays
        :param x: MNIST Training Images
        :param y: MNIST Training Labels
        :return: Tuple
        """
        # Using the numpy permutations method, create a permutation of the same size and apply it to both arrays
        perm = np.random.permutation(x.shape[0])
        return x[perm], y[perm]

    def calculate_accuracy(self):
        """
        Get the accuracy of the model by testing it on the given MNIST testing data
        :return: Float
        """
        x, y = self.testX, self.testY
        acc = 0
        for data in range(len(self.testY) // 2):
            s = self.predict(self.testX[data])
            if s == np.argmax(self.testY[data]):
                acc += 1
        return float((acc / (len(self.testX) // 2)) * 100)


if __name__ == "__main__":
    N = NeuralNetwork()

    trainx = (mnist.train_images() / 255).reshape(mnist.train_images().shape[0], 784)
    trainy = keras.utils.to_categorical(mnist.train_labels(), 10)

    N.train(trainx, trainy)
    print(N.calculate_accuracy())
