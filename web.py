import flask
import datetime
import random
import asyncio
from converter import converter as cv
from flask import *
from database import Database

site = Flask('Supplencer')

db = Database()


def find_supplencer(class_, day, hour):
    now = datetime.datetime.now().strftime('%A')
    current_day = cv.convert_days(1, now)
    if day == cv.convert_days(2, current_day):
        equal = True
    else:
        equal = False
    teacher_by_class = db.find_class_teachers(class_, equal)
    teacher_by_time = db.find_time_teachers(day, hour, equal)

    tbc = []
    tbt = []

    for item in teacher_by_class:
        tbc.append(item)
    for item in teacher_by_time:
        tbt.append(item)

    common_datas = {}

    def common_data(list1, list2):
        for x in list1:
            for y in list2:
                if x == y:
                    common_datas[x] = y
        for y in list2:
            for x in list1:
                if x == y:
                    common_datas[x] = y
        return common_datas

    data = common_data(tbc, tbt)

    try:
        choice = random.choice(list(data.keys()))
        return choice
    except IndexError:
        try:
            choice = random.choice(tbt)
            return choice
        except IndexError:
            return None


@site.route('/')
def index():
    return flask.render_template('index.html', show_='none')


@site.route('/sign')
def sign():
    return flask.render_template('sign.html', show_='none')


@site.route('/sign', methods=['post'])
def login():
    username = request.form['username'].title()
    password = request.form['password']

    if username == '' or password == '':
        return flask.render_template('sign.html', errors="I campi non posso essere vuoti!", show_='block')
    elif db.sign(username, password) and request.form['action'] == 'Firma':
        return flask.render_template('signed.html')
    elif request.form['action'] == 'Firma' and not db.sign(username, password):
        dbc, c = db.connect()
        email_raw = c.execute(
            'SELECT Email FROM Teachers WHERE username = ?', (username,))
        try:
            email = email_raw.fetchone()[0]
            dbc.close()
            if email == None:
                email = 'Non fornita'
        except TypeError:
            email = 'Non fornita'
        return flask.render_template('sign.html', errors="Username o Password non corretti!", show_='block', username=username, email=email)
    elif db.unsign(username, password) and request.form['action'] == 'Uscita anticipata':
        return flask.render_template('unsigned.html')
    else:
        return flask.render_template('sign.html')


@site.route('/', methods=['POST'])
def search():
    classe = request.form['classe']
    giorno = request.form['giorno']
    ora = request.form['ora']
    supplente = find_supplencer(classe, giorno, ora)
    if not supplente == None:
        supplencer = db.get_teacher_data(supplente)[1]
        return flask.render_template('index.html', supplencer=supplencer, text1='Il supplente per la classe ' + classe, text2='\u00E8:', show_='block', color_='black')
    elif supplente == None:
        return flask.render_template('index.html', text1='Non ho trovato un supplente!', text2='', show_='block', color_='#ff3d3d')
    else:
        return flask.render_template('index.html', show_='none')


@site.route('/restorepresences')
def restorepresences():
    db.restore_presences(asyncio.new_event_loop())
    return flask.redirect(url_for('index'))


if __name__ == '__main__':
    site.run(host='0.0.0.0', port='80')
