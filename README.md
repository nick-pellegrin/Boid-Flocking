# Particle-Motion-Sim

First pull this repo into a local project on your computer



Then, you will need to create a python virtual environment to store all of the dependencies.  To do this, run (in the root of your project dir) the command:

  $ python3 -m venv [name of virtual environment]
  
A good name for a virtual environment is:  'virtualenv'.
 
 
 
 
 
Next, you will need to activate your virtual environment in order to add packages to it and to access the dependencies during runtime.  To do this, navigate
to [name of your virtual directory]/Scripts and run the command: 
 
  $ activate
  
To deactivate, go to the Scripts directory again and type:
 
  $ deactivate
  
 
 
 
Next, you will need to download the dependencies from requirements.txt once your virtual environment is running.  To do this, run the command: 
 
  $ pip install -r requirements.txt
  
Note: when downloading new packages to your virtual environment, add them to the requirements.txt file by running the command: 

  $ pip freeze > requirements.txt
  
  
  
  
  
Finally, in order for your IDE to be able to access the dependencies located in the virtual environment, you will have to manually select the python interpreter.
The python interpreter you want is located in the virtual environment you just created in the Scripts folder, and the interpreter is named 'python.exe':

Example:  [name of your virtual env]/Scripts/python.exe
 
  
  
  

After all this set up is done, you should be able to simply run 'simulation.py' and start coding!
 
