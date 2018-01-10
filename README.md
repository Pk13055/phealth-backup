# Hostpital Management System

## Database setup

Since we are using postgresql for the backend connectivity, and want to avoid
possible conflicts and issues later on, please follow the same user convention
and schema for your config as well. 

- Installation

```
sudo apt install postgresql postgresql-contrib
```
- Add `nix` user 
```
sudo adduser hospital
```

- Database setup 

```
sudo -u postgres createdb hostpital
```
- Verify
```
sudo -i -u hospital psql # this will log you into the psql shell directly using
the corresponding user (uses ident login)
# once in the shell run:
\conninfo
```
You should get an output:
```
You are connected to "hostpital" as user "hospital" at port "5432"
```
- Change password
```
sudo -i -u hospital psql
\password hospital 
Enter password: root
Enter it again: root
```

At this point you're all set. The settings file has already been updated to
include this configuration. If you set up the user some other way, PLEASE add
your  config (`settings.py`) file to reflect the same, and add it to the
gitignore. This will prevent multiple changes over the course of the project,
BUT you will have to manually update the _other_ changes in this file.

- Dumping the database

Download the postgres.sql file from the drive and enter the hospital nix user
created. After that, run:
```
psql -U hospital hospital < postgresql.sql
```
All the tables will be created automatically.


## Python Setup

Assuming you're using a virtualenv (with virtualenvwrapper), run
```
mkvirtualenv hospital --python python3.6  # or whatever name you want
workon hospital
```

### Install Dependencies
```
pip3.6 install -r requirements.txt
```
