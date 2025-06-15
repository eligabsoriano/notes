# setup
1. Setup Virtual Environment:
    python3 -m venv venv
    source venv/bin/activate 

2. Install dependencies(create requirements.txt):
    requirements.txt
        django
        djangorestframework
        pillow

    pip install -r requirements.txt

3. Configure Database:
    python3 manage.py makemigrations
    python3 manage.py migrate

    python3 manage.py createsuperuser

# How to run

1. Active virtual environment:
    source venv/bin/activate  

    python3 manage.py runserver

command + l to open agent macos
ctrl + l to open agent on windows
