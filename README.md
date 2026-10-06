# task-manager

Django project for managing tasks, projects and workers

## Check it out:

[Task manager deployed to Render](https://task-manager-mwkg.onrender.com/)

## Installing 

Python3 must be already installed

```shell
git clone https://github.com/garamond1281/task-manager
cd task-manager
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata task_manager_data.json
python manage.py runserver

```

## Features

* Authentication functionality for Worker/User
* Managing projects, tasks & workers directly from website interface

##

Project Manager(Has permissions to create/update/delete tasks/projects/workers):

login: pm127

password: secret123


Developer(Has permissions to view tasks/projects/workers):

login: developer

password: secret4313

