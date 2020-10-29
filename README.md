# DigitRecognition
Created a Dense neural-network framework using Python and Numpy for Digit Analysis. Employed a web socket server to allow multiple users to interact with their own instance of a model as it progresses in terms of accuracy. Implemented GUI to allow the user to give input to the network and make predictions on their written text.


INSTRUCTIONS TO RUN THE PROGRAM:
  - Ensure all dependences are installed correctly
  - First, nagivatete to mvc.server and run Server.py 
    - If you plan to run the server remotely:
      - Change "server" in Server.py to the IP Address of machine the sever runs on
      - Note: Thre may be instances where your OS firewalls may block the existing connecting method using hostname, in that case:
            - Change the "server" state variable near the bottom of the Server.py file to the IPV4 of the machine running this server
                - Sample: server = "192.168.x.y" or any other valid IP
            - Next, navigate to the Client.py file in the same subpackage and change the class' "self.server" variable to the the IP of the machine running the server
            
  - Next, simply run main.py in the main directory
  - IMPORTANT NOTE: 
        - To connect multiple clients, you may have to use the terminal to run another instance of the main.py file, but if your IDE/environent allows, simply run another instance of main.py
   
  

DURING RUN TIME:
  - Mouse Right Click will "clear" the drawing box
  - The key 'w' will send the 'get_accuracy' message to the sever and update the accuracy on the GUI
  - Any other key press will send the 'prediction' message to the server and update the prediction tracker on the GUI
  - Note: Since almost no image processing was done on the user's end for the model, to see accruate results of the model, be sure to keep the image centered
  - Future commits will have button functionality for these tasks and better processing methods to keep the image centered in the data to the model, no matter where the user writes the digit!
