# DjangoEasyData - User list with PI Information
### With Randtronics DPM easyData API capabilities.
### Developed merely for demonstrations. Not for production.

## Deployment
### Prerequisite
1. Python 3.8
2. Git
3. OS - Linux/ Windows
4. MySQL 8
### Get the code.
```
git clone https://github.com/vchan-in/DjangoEasyData
cd DjangoEasyData
python3 -m venv .venv
source venv/bin/activate
pip install -r requirements.txt
```
### Configure the server
Example configuration in settings.py file.
```
# MYSQL DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'userlist',
        'USER': 'remote',
        'PASSWORD': 'remote',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

RANDTRONICS_EASYDATA_API = "https://192.168.2.144:8643"
RANDTRONICS_EASYDATA_AUTH_KEY = "YXBpdXNlcjphcGl1c2VyQDEyMw=="
RANDTRONICS_EASYDATA_CLIENT_USERNAME = "demoappnew"
RANDTRONICS_EASYDATA_CLIENT_PASSWORD = "demoappnew"
```
### Run the server
```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```
