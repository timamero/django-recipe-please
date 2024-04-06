# Recipe, Please!

## About The Project

Django web application that scrapes and displays recipe data from websites.

[See a demo of the website here](https://recipeplease-v2-b82eced00232.herokuapp.com/)

I created this project to practice web scraping with Beautiful Soup. The code to scrape the recipe site is in getrecipe/funcs.py. It can still be improved but it works fine for most recipe sites.

## Getting Started

### Dependencies

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
  ALLOWED_HOSTS
  DEBUG
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
