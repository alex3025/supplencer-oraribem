import sqlite3
import threading
import asyncio
import datetime
import time
from converter import converter
from threading import Timer


class Database:
    def __init__(self, database='teachers.db'):
        self.database = database
        self.converter = converter
        self.now = datetime.datetime.now()
        self.loop = asyncio.get_event_loop()

        threading.Thread(target=self.check_time).start()

    def connect(self):
        db = sqlite3.connect(self.database)
        c = db.cursor()
        return db, c

    def check_time(self):
        print('Loop Started!')
        restored = False
        while True:
            if self.now.hour == 17 and self.now.minute in range(6) and restored == False:
                print('Presences Restored!')
                self.restore_presences(self.loop)
                restored = True
            time.sleep(1)

    def restore_presences(self, loop):
        async def func():
            db, c = self.connect()
            c.execute('SELECT Presenza FROM Teachers')
            presences = c.fetchall()
            for item in presences:
                c.execute('UPDATE Teachers SET Presenza = ?', ('no',))
                db.commit()
            db.close()

        threading.Thread(target=lambda loop: loop.run_until_complete(
            func()), args=(loop,)).start()

    def get_teacher_data(self, id_):
        db, c = self.connect()
        c.execute('SELECT * FROM Teachers WHERE id = ?', (id_,))
        data = c.fetchall()
        return list(data[0])

    def sign(self, username, password):
        db, c = self.connect()
        c.execute(
            'SELECT Id FROM Teachers WHERE username = ? AND password = ?', (username, password))
        data = c.fetchone()
        db.close()
        if data:
            db, c = self.connect()
            c.execute('UPDATE Teachers SET Presenza = ? WHERE username = ? AND password = ?',
                      ('si', username, password))
            db.commit()
            db.close()
            return True
        else:
            return False

    def unsign(self, username, password):
        db, c = self.connect()
        c.execute(
            'SELECT Id FROM Teachers WHERE username = ? AND password = ?', (username, password))
        data = c.fetchone()
        db.close()
        if data:
            db, c = self.connect()
            c.execute('UPDATE Teachers SET Presenza = ? WHERE username = ? AND password = ?',
                      ('no', username, password))
            db.commit()
            db.close()
            return True
        else:
            return False

    def find_class_teachers(self, class_=None, equal=None):
        db, c = self.connect()
        c.execute('SELECT Classi, Id, Presenza FROM Teachers')
        classes = c.fetchall()
        db.close()
        all_classes = {}
        teachers = {}
        for _class, teacher, presenza in classes:
            if presenza == 'si' and not equal:
                all_classes[teacher] = _class.split(' ')
            elif presenza == 'no' and equal:
                all_classes[teacher] = _class.split(' ')
        if not class_ == None:
            for item in all_classes:
                if class_ in all_classes[item]:
                    teachers[item] = all_classes[item]
            return teachers
        else:
            return all_classes

    def find_time_teachers(self, day=None, hour=None, equal=None):
        db, c = self.connect()
        c.execute('SELECT Orari, Id, Presenza FROM Teachers')
        times = c.fetchall()
        db.close()
        all_times = {}
        common_times = {}
        for time, teacher, presenza in times:
            if presenza == 'si' and not equal:
                all_times[teacher] = time.split(' ')
            elif presenza == 'no' and equal:
                all_times[teacher] = time.split(' ')
        if day and hour:
            for item in all_times:
                if day + '.' + hour in all_times[item]:
                    common_times[item] = all_times[item]
            return common_times
        else:
            return all_times
