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
## Descripton

Task Management System (Django)

A robust and feature-rich Task Management Web Application built with Python and Django.
Designed for teams and project managers to efficiently track projects, manage worker profiles,
assign tasks, and monitor task progress with optimized database performance.

## Features

* User Authentication & Role-Based Access Control: Secure login/logout flows, custom user profiles, and strict permissions (e.g., standard users can only edit their own profiles, while Project Managers have elevated privileges using UserPassesTestMixin).

* Project & Task Tracking: Create and manage projects, organize tasks by types, and categorize them into active (in-progress) and completed statuses.

* Worker Directory: Comprehensive worker profiles displaying assigned tasks, contact info, and positions.

* Advanced Query Optimization: Performance-tuned using select_related, prefetch_related (with custom Prefetch objects), and split aggregation queries to completely eliminate N+1 query bottlenecks.

* Modern UI/UX: Styled with Bootstrap 5 and Bootstrap Icons, featuring responsive layouts, custom sidebars, and interactive table components.

## Database Schema

![Database Diagram](/db_diagram.png)

##

Project Manager(Has permissions to create/update/delete tasks/projects/workers):

login: pm127

password: secret123


Developer(Has permissions to view tasks/projects/workers):

login: developer

password: secret4313

