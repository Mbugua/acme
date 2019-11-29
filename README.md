# Acme
Bus Booking Application developed in Python Django.

# Website
https://bus-acme.herokuapp.com/

## By **[Lee Mbugua](https://github.com/Mbugua)**

## Description
[This] (https://bus-acme.herokuapp.com/) is a web application that allows users to search for buses by entering their starting point and destination. The results list has buses arranged with the cheapest bus at the top of the list. The user can select a bus and book a seat in the bus.

## User Story:
* search for a bus by entering the departure location and arrival location
* select a bus
* see information on the selected bus
* pay for the selected bus and get a ticket

## Specifications
| Behavior        | Input           | Outcome  |
| ------------- |:-------------:| -----:|
| Search for a bus | Departure location: Nakuru <br> <br> Arrival Location: Nairobi <br> <br> Travel Date: 02/02/2018 | Display list of buses found |
| Select a bus | Click **select** button | Display information about the selected bus and a form for user to input their information |
| Get a ticket | Click **confirm and book** | Display pdf with ticket information |

## Setup/Installation Requirements

### Prerequisites
* Python 3.7.5
* Django 2.2.5
* Virtual environment
* Postgres Database
* Internet

### Installation Process
1. Copy repolink
2. Run `git clone REPO-URL` in your terminal
3. Write `cd buupass_acme`
4. Create a virtual environment with `virtualenv virtual` or try `python3.6 -m venv virtual`
5. Create .env file `touch .env` and add the following:
```
SECRET_KEY=<your secret key>
DEBUG=True
```
6. Enter your virtual environment `source virtual/bin/activate`
7. Run `pip install -r requirements.txt` or `pip3 install -r requirements.txt`
8. Create Postgres Database

```
psql
CREATE DATABASE bupass_acme
```
9. Change the database informatioin in `/settings.py`
Local setup
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASS'),
        'HOST': config('DB_SERVICE'),
        'PORT': config('DB_PORT'),
    }
}
```
10. Run `./manage.py runserver` or `python3.6 manage.py runserver` to run the application

11. TO DO
- Mobile payments
- Send SMS notification
- Finalize Tickets
```
## Known Bugs
* open ticket :P

## Technologies Used
- Python 3.7.5
- Django 2.2.5
- Bootstrap 4
- Postgres Database
- Heroku
- Africa's Talking API

## License
- Open
