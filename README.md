
# semester-project-team-5

## Wallecom
Wallecom is an ecommerce platform, that is targeted towards the Puerto Rican people.  

## TEAM

* Stephanie Vargas
* Coralys M. Cortes 
* Francisco Valentin
* Hector G Aponte 
* Waldemar J Reyes 
* Angel F Zayas 

## Getting Started

This instructions will help, in having this project running on your local machine for deployment and testing purposes.

### Prerequisites

Software products and packages with their versions, that need to be installed on your machine, in order to run this project are:

python = 3.9.1

pip = 21.0.1

For more information on how to download and install pip, go to the following link:

https://pip.pypa.io/en/stable/installing/

Django = 3.1.6:

```
python3 -m pip install Django
```
For image handling, Pillow >= 8.1.0:

```
python3 -m pip install Pillow
```

postgresSQL = 13.2

For more information on how to download and install postgresSQL, go to the following link:

https://www.postgresql.org/download/

```
pip install psycopg2
```

In an older/legacy computer the command is: 

```
pip install psycopg2-binary
```

### Running

In order to run the project a database needs to be created using the SQL shell that was downloaded when postgresSQL was installed. The SQL shell, can be opened from the MAC spotlight (command + space) or Windows run as (windows key + R) and typing SQL shell. Once opened it will ask for some prompts (including a password), they don't need to be filled unless it was given in installation, so just press enter. After that to create the database needed to run this projects, run this commands inside (the SQL shell):


```
 create database ecommerce;
 create user ecommerce_user with password 'ecuser123';
 alter database ecommerce owner to ecommerce_user;
```

Once this commands were given the database is created and the project can be runned. 

### In MACOS

To run this project in MAC, first clone or download this repository, after navigating to this project, use the following commands to start the project and virtual environment: 

```
 cd django_mm
 source venv/bin/activate
 cd src
 python manage.py makemigrations
 python manage.py migrate
 python manage.py runserver
```


## Built with 

* [Django] - Python Web framework

## Acknowledgments

* Bootstrap - https://getbootstrap.com/docs/5.0/getting-started/introduction/

* Font Awesome - https://fontawesome.com/start

* Justin Mitchell - Coding Entreprenaur & Teacher






