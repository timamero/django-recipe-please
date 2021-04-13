# Recipe, Please!
Django web application that scrapes and displays recipe data from websites.

[See a demo of the website here](https://recipeplease.herokuapp.com/getrecipe/)

I created this project to practice web scraping with Beautiful Soup. The code to scrape the recipe site is in getrecipe/funcs.py. It can still be improved but it works fine for most recipe sites.

## Instructions
Clone this project
```
https://github.com/timamero/django-recipe-please.git
```

Install Dependencies
```
pip install -r requirements.txt
```
Note: This project was configured with postgresql. Update database settings if you will not be using postgresql
Update settings.py Variables
```
SECRET_KEY 
DATABASES['default']['Name']
DATABASES['default']['User']
DATABASES['default']['Password']
```

Run Database Migrations 
```
py manage.py makemigrations
py manage.py migrate
```

Create Superuser
```
py manage.py createsuperuser
```
