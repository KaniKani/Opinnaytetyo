# Opinnaytetyo / Thesis
Robot Framework sulautetuissa järjestelmissä / The Robot Framework in embedded systems

To start testing embedded systems, copy the file structure of this repository. With the commande "git clone https://github.com/KaniKani/Opinnaytetyo.git" in your Linux terminal

You will need some packages for anything to work so install Python3 via the command "sudo apt install python3" in the Linux terminal. Note that the command may vary a little depending on which Linux package management system you are using.

After installing python, install pip via the command "sudo apt install python3-pip"

Now with the required python packages installed in the system, we will create a python virtual environment with the command "python3 -m venv <venv>" where <venv> is the name of the virtual environment. Make sure you are inside the Opinnaytetyo directory before executing the command.

After the virtual environment is created, we can enter with the command "source <venv>/bin/activate" where <venv> is the name of the virtual environment. To leave the environment, use the command "deactivate".

Now with pip installed and we are inside the virtual environment. We can install the pip packages within requirements.txt with the command "pip install -r requirements.txt"

To Flash the ESP32, use Arduino IDE with the correct settings for your board or use VS Code if you have it set up for flashing microcontrollers. Use the isotest.ino file from the serial_tests directory for Serial testing.

After flashing the ESP32, change the correct port where it is connected to in the serialtest.robot file. After changing the port, you can navigate to Opinnaytetyo/serial_test/tests and start the test via the command "robot serialtest.robot".

Happy testing :)
