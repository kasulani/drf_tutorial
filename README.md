# Music Service API
## About
This is a simple music service API that I created as an example for a [tutorial](https://medium.com/backticks-tildes/lets-build-an-api-with-django-rest-framework-32fcf40231e5) for
learning Django REST Framework.
## Goal
The goal of this project is teach Django REST framework on novice programmers.
## Features
With this API;
- You can create, view, update, and delete a song
## Technology stack
Tools used during the development of this API are;
- [Django](https://www.djangoproject.com) - a python web framework
- [Django REST Framework](http://www.django-rest-framework.org) - a flexible toolkit to build web APIs
- [SQLite](https://www.sqlite.org/) - this is a database server
## Requirements
- Use Python 3.x.x+
- Use Django 2.x.x+
## Tests
"Code without tests is broken as designed", said  [Jacob Kaplan-Moss](https://jacobian.org/writing/django-apps-with-buildout/#s-create-a-test-wrapper). Therefore i shall not give you code that
can not be tested or has no tests. So, to run tests, enter the following command
```sh 
    $ python manage.py test
```
## Running the application
To run this application, clone the repository on your local machine and execute the following command.
```sh
    $ cd music_service
    $ virtualenv virtenv
    $ source virtenv/bin/activate
    $ pip install -r requirements.txt
    $ python manage.py makemigrations
    $ python manage.py migrate
    $ nohup python manage.py runserver & disown
```
