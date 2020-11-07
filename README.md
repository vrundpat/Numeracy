# Numeracy: Image Analysis
A Dense Neural Network (DNN) Framework built using pure Python which comes integreated into a socket server that utilizes threading to support & provide multiple concurrent users with an instance of their own neural network! Accompanied by a PyGame GUI, users can give their NN instance inputs in forms of hand written digits and train the network! The mixture of MNIST, Sci-kit databses along with human induced inputs results in some pretty accurate predictions from the NN, achieving 96% accuracy on user inputs, and near perfect accuracy on the data sets.

Below are some samples of the GUI, although its not best representative of the code, it captures the gist of the program's aim! These are samples of digits written by me and overtime the DNN becomes extremely accurate. It reaches nearly a perfect accuracy on the MNIST data set, but as human induced input is more unpredictable, its not quite perfect but it's close!
\n
| Start with this  | End with this! | End with this! | End with this! |
| ------------- | ------------- | ------------- | ------------- |
| ![ScreenShot](https://raw.github.com/vrundpat/Numeracy/master/Previews/BadPredict1.png) | ![ScreenShot](https://raw.github.com/vrundpat/Numeracy/master/Previews/GoodPredict0.png)  | ![ScreenShot](https://raw.github.com/vrundpat/Numeracy/master/Previews/GoodPredict2.png) | ![ScreenShot](https://raw.github.com/vrundpat/Numeracy/master/Previews/GoodPredict8.png)  |


## INSTRUCTIONS TO RUN THE PROGRAM:
  - Ensure all dependences are installed correctly
  - First, nagivatete to mvc.server and run Server.py 
    - If you plan to run the server remotely:
     - Change ```server``` in ```Server.py``` to the IP Address of machine the sever runs on
        - Note: Thre may be instances where your OS firewalls may block the existing connecting method using hostname, in that case:
     - Change ```server``` variable near the bottom of the ```Server.py``` to the IPV4 of the machine running this server
                - Sample: ```server = "192.168.x.y"``` or any other valid IP
            - Next, navigate to the Client.py file in the same subpackage and change the class' ```self.server``` variable to the the IP of the machine running the server
            
  - Next, simply run ```main.py``` in the main directory
  #### IMPORTANT NOTE: 
  - To connect multiple clients, you may have to use the terminal to run another instance of the main.py file, but if your IDE/environent allows, simply run another instance of main.py
   
  

## DURING RUN TIME:
  - ```Mouse Right Click``` will "clear" the drawing box
  - The key ```'w'``` will send the ```get_accuracy``` message to the sever and update the accuracy on the GUI
  - ```Any other key press``` will send the ```prediction``` message to the server and update the prediction tracker on the GUI
  - Note: Since almost no image processing was done on the user's end for the model, to see accruate results of the model, be sure to keep the image centered
  - Future commits will have button functionality for these tasks and better processing methods to keep the image centered in the data to the model, no matter where the user writes the digit!
