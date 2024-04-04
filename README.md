# Recipe, Please!

## About The Project

Django web application that scrapes and displays recipe data from websites.

[See a demo of the website here](https://recipeplease.herokuapp.com/getrecipe/)

I created this project to practice web scraping with Beautiful Soup. The code to scrape the recipe site is in getrecipe/funcs.py. It can still be improved but it works fine for most recipe sites.

## Getting Started

### Dependencies

- PostgreSQL ([Install PostgreSQL](https://www.postgresql.org/download/))

This project was configured with PostgreSQL. It is required to use the ArrayField type in Models. [See steps to set up PostreSQL in Django here](https://github.com/timamero/django-starting-template/blob/main/postgresql/configure-postgresql-database.md)

### Installation

- Clone this project

  ```
  https://github.com/timamero/django-recipe-please.git
  ```

- Create virtual environment

  ```
  py -m venv venv
  ```

- Install Dependencies

  ```
  pip install -r requirements.txt
  ```

- Update the following settings.py variables

  ```
  SECRET_KEY
  DATABASES['default']['Name']
  DATABASES['default']['User']
  DATABASES['default']['Password']
  ```

  - To generate a new secret key, enter the following into the command line:
    ```
    python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
    ```

- Run Database Migrations

  ```
  py manage.py makemigrations
  py manage.py migrate
  ```

- Create Superuser

  ```
  py manage.py createsuperuser
  ```

- Run server
  ```
  py manage.py runserver
  ```
