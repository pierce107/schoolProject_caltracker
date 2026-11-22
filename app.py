
import pymysql
from datetime import date, datetime timedelta

from flask import (Flask, redirect, render_template, url_for)

app = Flask (__name__)

meals = ['Frühstück', 'Mittagsessen', 'Abendessen', 'Snacks']
genders = ['Männlich', 'Weiblich', 'Divers']
activities = [
    ('Wenig aktiv', 'Überwiegend sitzend'),
    ('Mäßig aktiv', '1-3 Trainings / Woche'),
    ('Sehr aktiv', '4+ Trainings / Woche'),
]
months = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli',
          'August', 'September', 'Oktober', 'November', 'Dezember']
weekdays = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag',
            'Samstag', 'Sonntag']

@app.route('/')
@app.route('/index.html')
def index():
    today =  date.today()
    return render_template(
        'index.html', heading=heading, is_today=current == today,
        date_long=date_long(current), date_short=date_short(current),
        current_date=current.isoformat(),
        prev_date=(current - timedelta(days=1)).isoformat(),
        next_date=(current + timedelta(days=1)).isoformat(),
    )

def date_long(d):
    return f'{weekdays[d.weekday()]}, {d.day}. {months[d.month - 1]} {d.year}'


def date_short(d):
    return f'{weekdays[d.weekday()][:2]}., {d.day}. {months[d.month - 1]}'

