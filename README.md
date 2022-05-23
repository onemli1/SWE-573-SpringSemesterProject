# SWE-573-SpringSemesterProject
This repository is created for SWE573 project.
## CoLearn

This website is designed as a platform where people can share what they want to teach each other.The expectation of students is their unsupressed eagerness to learn.
The website do not contain any payment or credit system.

There will be also an event option to make people meet and share some funny time.

To get the source code on your local machine, you can use 
```git init``` command, and then ```https://github.com/onemli1/SWE-573-SpringSemesterProject.git``` command.

To run the system locally, there should be an ide to open the code like Visual Studio code and PostgreSql for the database. Docker desktop should also be installed because docker commands cannot be run without it. To create the virtual environment for the project, ```source myvenv/bin/activate``` command should be run on the project directory in the terminal. All the requirements should be installed to use the system. The needed installations are given in the requirements.txt file, so just by running ```pip install -r requirements.txt``` command, the process can be completed.When we clone from git system, the database will be running according to the docker system( colearn/setting).You will see the following part:

'''# POSTGRES database is used for this project'''
'''# This setup is for DOCKER's postgres image'''


'''DATABASES = {'''
    '''default': {'''
       '''ENGINE': 'django.db.backends.postgresql','''
       '''NAME': 'postgres','''
       '''USER': 'postgres','''
       '''PASSWORD': 'postgres','''
       '''HOST': 'pgdb','''
       '''PORT': 5432,'''
    '''}'''
'''}'''

If you want runnig with docker. To run the system locally with a local postgresql database, localhost could be given there. To create the database for Docker, some commands should also be run. Firstly, create a database on your local machine. Run ```docker-compose up --build``` command to build the Docker images. Then, ```docker-compose start db``` should be run to start the db. To run the images for Docker, ```docker-compose up``` should be run. If you want the run to be continued in the background, you can run the ```docker-compose up -d``` command. 

If you want without docker running. You have to make local database configurations.You can see in colearn file setting part:

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

"""
DB_NAME = "colearn_db"
DB_USER = "django"
DB_PASSWORD = "pass1234"
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'DB_NAME',
        'USER': 'DB_USER',
        'PASSWORD': 'DB_PASSWORD',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
"""



The system also has an admin side. So, to create an admin user, please run the command ```python manage.py createsuperuser```.

The system can be reachable from http://127.0.0.1:80/ link. The “python manage.py runserver” command is not needed to be run because it is written in the Dockerfile. All needed commands to do migrations for the database are also written there.
