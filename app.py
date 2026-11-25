from datetime import date, datetime, timedelta

from flask import (Flask, redirect, render_template, request, url_for)

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
    current = parse_date(request.args.get('date'))
    today =  date.today()

    delta = (current - today).days
    heading = {0: 'Heute', -1: 'Gestern', 1: 'Morgen'}.get(delta, 'Tagesübersicht')
    kcal = {'consumed': 650, 'target': 2400, 'pct': 27, 'bar': 27, 'diff': 1750, 'over': False}
    prot = {'consumed': 42.5, 'target': 150, 'pct': 28, 'bar': 28, 'diff': 107.5, 'over': False}
    dummy_meals = [
        {
            'name': 'Frühstück',
            'kcal': 420,
            'protein': 28.0,
            'logs': [
                {'id': 1, 'name': 'Haferflocken', 'amount_g': 80, 'kcal': 298, 'prot': 10.8},
                {'id': 2, 'name': 'Magerquark', 'amount_g': 180, 'kcal': 122, 'prot': 21.6},
            ],
        },
        {'name': 'Mittagsessen', 'kcal': 0, 'protein': 0.0, 'logs': []},
        {'name': 'Abendessen', 'kcal': 0, 'protein': 0.0, 'logs': []},
        {'name': 'Snacks', 'kcal': 0, 'protein': 0.0, 'logs': []},
    ]
    quick = [
        {'id': 1, 'name': 'Haferflocken', 'meal': 'Frühstück', 'amount': 80},
        {'id': 2, 'name': 'Magerquark', 'meal': 'Frühstück', 'amount': 250},
    ]
    foods_json = [
        {'id': 1, 'name': 'Haferflocken', 'kcal': 372},
        {'id': 2, 'name': 'Magerquark', 'kcal': 68},
    ]
    selected_meal = request.args.get('meal')
    if selected_meal not in meals:
        selected_meal = meals[0]

    return render_template(
        'index.html', heading=heading, is_today=(current == today),
        date_long=date_long(current), date_short=date_short(current),
        current_date=current.isoformat(),
        prev_date=(current - timedelta(days=1)).isoformat(),
        next_date=(current + timedelta(days=1)).isoformat(),
        kcal=kcal, prot=prot, meals=dummy_meals, meal_names=meals,
        has_history=True, quick=quick, foods_json=foods_json,
        selected_meal=selected_meal,
    )

@app.route('/lebensmittel.html')
def lebensmittel():
    return render_template('lebensmittel.html')

@app.route('/profil.html')
def profil():
    return render_template('profil.html')

@app.route('/add_log', methods=['POST'])
def add_log():
    return redirect(url_for('index', date=request.form.get('date')))

@app.route('/edit_log/<int:id>', methods=['GET', 'POST'])
def edit_log(id):
    return redirect(url_for('index'))

@app.route('/delete_log/<int:id>', methods=['POST'])
def delete_log(id):
    return redirect(url_for('index'))

def date_long(d):
    return f'{weekdays[d.weekday()]}, {d.day}. {months[d.month - 1]} {d.year}'

def date_short(d):
    return f'{weekdays[d.weekday()][:2]}., {d.day}. {months[d.month - 1]}'

def parse_date(raw):
    try:
        return datetime.strptime(raw, '%Y-%m-%d').date()
    except (TypeError, ValueError):
        return date.today()

def de_int(value):
    return f'{int(value):,}'.replace(',', '.')

def de_dec(value):
    text = f'{float(value):,.1f}'.replace(',', '§').replace('.', ',').replace('§', '.')
    return text[:-2] if text.endswith(',0') else text

def initials(name):
    parts = (name or '').split()
    if not parts:
        return '?'
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[1][0]).upper()

app.jinja_env.filters.update(de_int=de_int, de_dec=de_dec, initials=initials)

if __name__ == '__main__':
    app.run(debug=True)
