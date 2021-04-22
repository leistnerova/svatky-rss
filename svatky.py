#!/usr/bin/env python

from datetime import datetime, timedelta
import configparser
import os
import psycopg2
import sys

sys.path.append(os.path.split(__file__)[0])


def application(environ, start_response):
    config = configparser.ConfigParser()
    # config.read('{}/.config/config.ini'.format(os.path.split(__file__)[0]))
    config.read('.config/config.ini')

    result = '<channel>'

    conn = psycopg2.connect(
        (
            'dbname={db} user={user} password={passw}'
        ).format(
            db=config['db']['database'],
            user=config['db']['user'],
            passw=config['db']['password']
        )
    )
    db = conn.cursor()
    today = datetime.today().strftime('%d.%-m.')
    yesterday = datetime.today() - timedelta(days=1)
    yesterday = yesterday.strftime('%d.%-m.')
    db.execute('select * from svatky where datum=%s', [today])
    row = db.fetchone()
    result += '<item><title>Today</title><description>{} / {}</description>' \
        '<guid>{}</guid></item>'
    result = result.format(row[1], row[2], today)
    db.execute('select * from svatky where datum=%s', [yesterday])
    row = db.fetchone()
    result += '<item><title>Yesterday</title><description>{} / {}</description>' \
        '<guid>{}</guid></item>'
    result = result.format(row[1], row[2], yesterday)

    start_response('200 OK', [('Content-Type', 'text/xml')])
    result += '</channel>'
    result = bytes(
        '<?xml version="1.0" encoding="utf-8"?>\n<rss version="2.0">\n{}\n'.format(result)
    )

    conn.close()

    return [result]
