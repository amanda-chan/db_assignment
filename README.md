# Team 26: EatWhere – Food Reviews & Reservations Application

## Pre-requisites
Before running the application, ensure that you have downloaded the source code in a folder <br>
The following applications are to be installed and setup:
<ul>
  <li><a href="https://code.visualstudio.com/download">Visual Studio Code</a></li>
  <li><a href="https://dev.mysql.com/downloads/mysql/">MySQL Community Server</a> (Relational Database) </li>
  <li><a href="https://www.mongodb.com/try/download/community">MongoDB</a> (Non-Relational Database) </li>
  <li><a href="https://www.python.org/downloads/">Python</a> - during installation ensure to add python to path </li>
</ul>

## VS Code setup

### Step 1: Open up the Visual Studio Code application
![image](https://github.com/amanda-chan/db_assignment/assets/60087811/b13f4f09-1313-40c6-971d-cc4e6e6a7f0a)

### Step 2: Naviagte to extensions and install Python
![image](https://github.com/amanda-chan/db_assignment/assets/60087811/cbbd95ea-e016-4b27-bff4-ff8bce1246d5)

### Step 3: Open up the source code folder (File > Open Folder)
![image](https://github.com/amanda-chan/db_assignment/assets/60087811/24c3a0eb-27d5-4452-8a82-a0a39862e1e9)


### Step 4: Create the virtual enviroment 
#### Open the Command Palette (Ctrl+Shift+P), search for the "Python: Create Environment" command, and select it.
![image](https://github.com/amanda-chan/db_assignment/assets/60087811/a65a1367-0e48-4013-a761-74a878a8f3e1)

#### Select venv
![image](https://github.com/amanda-chan/db_assignment/assets/60087811/8a21db6b-8d1f-423a-9bfe-1d552bd4e34b)

#### Select the intepreter of the latest python version that you have added to path
![image](https://github.com/amanda-chan/db_assignment/assets/60087811/ea5aafa3-dc6a-437d-a1aa-02671c0936bc)


#### On success, when you open a new terminal (Terminal > New Terminal), it will show that the virtual enviroment has been activated
![image](https://github.com/amanda-chan/db_assignment/assets/60087811/07029f29-c9e2-43f5-a090-028516542959)



## Installing relevant libraries & packages

### In the terminal type the command below to install the packages (this might take a few minutes)
```bash
pip install -r requirements.txt
```
![image](https://github.com/amanda-chan/db_assignment/assets/60087811/6e3b8dcb-a616-48de-818e-344b775e4555)


### If any new packages are added to the requirements.txt file, use
```bash
pip freeze > requirements.txt
```

## Database setup

### Open the food_app folder and navigate to the file __init__.py
![image](https://github.com/amanda-chan/db_assignment/assets/60087811/aabab235-1ec4-4c34-a5ae-84465cd1ef9e)


### Change line 22 (relational db) and line 42 (non-relational db) accordingly to the credentials and setting of your local databases
![image](https://github.com/amanda-chan/db_assignment/assets/60087811/719a98f5-5b0d-44e6-b173-544791e1e6ef)


### Save the file (Ctrl + s), after you're done editing

## Running the application

### Head back to the terminal and type the following command
```bash
flask --app food_app --debug run
```
![image](https://github.com/amanda-chan/db_assignment/assets/60087811/33148125-5213-4ffd-aa69-d739bfa37c93)


### Copy the address from the terminal into your browser and you should be able to see the application!
![image](https://github.com/amanda-chan/db_assignment/assets/60087811/2f86e9e1-abdd-46a7-91ff-43c0144affb4)


