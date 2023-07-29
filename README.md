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
![image](https://github.com/amanda-chan/db_assignment/assets/60087811/c3670d84-cf71-497c-a374-dee4761fa619)

### Step 2: Naviagte to extensions and install Python
![image](https://github.com/amanda-chan/db_assignment/assets/60087811/f613609b-1507-4e64-a020-c478d14dcd95)

### Step 3: Open up the source code folder (File > Open Folder)
![image](https://github.com/amanda-chan/db_assignment/assets/60087811/b48e3385-fdb5-4d6f-a8b7-abbd56b07092)

### Step 4: Create the virtual enviroment 
#### Open the Command Palette (Ctrl+Shift+P), search for the "Python: Create Environment" command, and select it.
![image](https://github.com/amanda-chan/db_assignment/assets/60087811/2d8e30d6-2476-4ada-a563-44ce0ecc8315)
#### Select venv
![image](https://github.com/amanda-chan/db_assignment/assets/60087811/67e02a27-7d01-4467-a7b3-6e4792e944b6)
#### Select the intepreter of the latest python version that you have added to path
![image](https://github.com/amanda-chan/db_assignment/assets/60087811/1d6eb8a7-e55d-43bd-aa37-3971ce101a4e)
#### On success, when you open a new terminal (Terminal > New Terminal), it will show that the virtual enviroment has been activated
![image](https://github.com/amanda-chan/db_assignment/assets/60087811/819521eb-1161-42bd-9936-4176cb17ad85)

## Installing relevant libraries & packages

### In the terminal type the command below to install the packages (this might take a few minutes)
```bash
pip install -r requirements.txt
```
![image](https://github.com/amanda-chan/db_assignment/assets/60087811/82519dad-3d2e-485f-8d70-e85b04c45e63)

### If any new packages are added to the requirements.txt file, use
```bash
pip freeze > requirements.txt
```

## Database setup

### Open the food_app folder and navigate to the file __init__.py
![image](https://github.com/amanda-chan/db_assignment/assets/60087811/2e23972a-cd12-41f2-940f-236ba7d6c905)

### Change line 22 (relational db) and line 42 (non-relational db) accordingly to the credentials and setting of your local databases
![image](https://github.com/amanda-chan/db_assignment/assets/60087811/ceaedf04-e8cb-475c-98d9-e091f7053e35)

### Save the file (Ctrl + s), after you're done editing

## Running the application

### Head back to the terminal and type the following command
```bash
flask --app food_app --debug run
```
![image](https://github.com/amanda-chan/db_assignment/assets/60087811/82ef4361-1e1a-4c0c-8927-fae9b50ece7d)

### Copy the address from the terminal into your browser and you should be able to see the application!
![image](https://github.com/amanda-chan/db_assignment/assets/60087811/695d7a6b-8047-4d5e-b915-1fa1835ecee2)

