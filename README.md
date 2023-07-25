# db_assignment

### Figma
<a href="https://www.figma.com/file/U2bY5qkUmypBeqRf6U22C0/db-assignment?type=design&node-id=0%3A1&t=RIGuVeDA5wz7yWGq-1">figma link</a>


## Database setup
### MySQL
create database (haven't test CRUD, just for connection)

```bash
CREATE DATABASE IF NOT EXISTS foodappdb;
```

create user

```bash
CREATE USER 'db_project'@'localhost' IDENTIFIED BY 'password';
```

grant permissions

```bash
GRANT ALL ON foodappdb.* TO 'db_project'@'localhost';
```


## Flask setup
setup .venv: in vscode, click ctrl + shift + p

install packages from requirements if vscode didn't let you select

```bash
pip install -r requirements.txt
```

if installed any new python packages, update requirements.txt

```bash
pip freeze > requirements.txt
```

## Update on html
navbar.html is included in base.html, don't need to add in individual pages anymore!


## Run app

```bash
flask --app food_app --debug run
```


## Flask Migration
For new updates to the mysql db model:
Ensure that you have installed "Flask-Migration"

```bash
pip install Flask-Migrate
```

To create a new migration (scan any changes in models.py)

```bash
flask --app food_app db migrate -m '<migration name>'
```

Update the db based on the latest migration

```bash
flask --app food_app db upgrade
```
If it does not work, it means you have to manually add the changes into the db yourself TT (or delete the db in sql and run the app again which will initialise everything again) (Even though this was supposed to help with it). Then run upgrade command :D
