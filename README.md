# DigitRecognition
- Created a Dense neural-network framework using Python and Numpy.
- Used supervised training and backpropagation to train the model on the MNIST Database.
- Using python sockets and threading, deploy the model onto a server instance in order to allow 
multiple user interactions
- PyGame GUI is provided so the users can give input to the model in terms of hand-written digits
for model classification purposes.

Instructions to run:
  - Ensure all dependences are installed correctly
  - First, nagivatete to mvc.server and run Server.py 
    - If you plan to run the server remotely:
      - Change "server" in Server.py to the IP Address of machine the sever runs on
      
  - Next, simply run main.py in the main directory
  

During run time:
  - The key 'w' will send the 'get_accuracy' message to the sever and update the accuracy on the GUI
  - Any other key press will send the 'prediction' message to the server and update the prediction tracker on the GUI
  - Note: Future commits will have button functionality for these tasks!
