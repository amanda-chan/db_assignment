# db_assignment

<a href="https://www.figma.com/file/U2bY5qkUmypBeqRf6U22C0/db-assignment?type=design&node-id=0%3A1&t=RIGuVeDA5wz7yWGq-1">Figma Link</a>


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
run after .venv is created
```bash
pip install -r requirements.txt
```

## Run app
```bash
flask --app food_app --debug run
```

## Reuse navbar code
Reuse navbar code accross all pages (include this in the head tag or start of body tag)
```bash
<script src="<%= url_for('static', 'js/navbar.js') %>"></script>
```

## Flask Migration
For new updates to the mysql db model
```bash
<script src="<%= url_for('static', 'js/navbar.js') %>"></script>
```
