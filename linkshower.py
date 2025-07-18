#! /usr/bin/env python3

import sqlite3
import os
from flask import Flask
from flask import render_template
from flask import redirect

app = Flask(__name__)

db_path = '{}links.db'.format(os.getenv('IRC_db_path', './'))
channel = os.getenv('IRC_channel', '#linkgrabber')
server = os.getenv('IRC_server', 'irc.libera.chat')

@app.route('/')
def index():
    return redirect('/1')

@app.route('/<int:page_id>')
def page(page_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    links = []

    limit = str(20)
    offset = str((page_id * 20) - 20)

    for row in c.execute('''SELECT * FROM links ORDER BY rowid
                            DESC LIMIT {} OFFSET {}'''.format(limit, offset)):
        links.append(row)

    c.close()

    next_page = page_id + 1
    if page_id - 1 < 1:
        previous_page = 1
    else:
        previous_page = page_id - 1

    return render_template('links.html',
                            links=links,
                            server=server,
                            channel=channel,
                            next_page=next_page,
                            previous_page=previous_page)

@app.route('/<nick>')
def nick_base_page(nick):
    return redirect('/{}/1'.format(nick))

@app.route('/<nick>/<int:page_id>')
def nick_page(nick, page_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    links = []

    limit = str(20)
    offset = str((page_id * 20) - 20)

    for row in c.execute('''SELECT * FROM links WHERE nick = "{}" ORDER BY rowid
                            DESC LIMIT {} OFFSET {}'''.format(nick, limit, offset)):
        links.append(row)

    c.close()

    next_page = page_id + 1
    if page_id - 1 < 1:
        previous_page = 1
    else:
        previous_page = page_id - 1

    return render_template('links.html',
                            links=links,
                            server=server,
                            channel=channel,
                            nick=nick,
                            next_page=next_page,
                            previous_page=previous_page)

@app.route('/top')
def top_sites():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    top_sites = []

    for row in c.execute('''SELECT 
                            CASE 
                                WHEN url LIKE 'http://%' THEN 
                                    CASE 
                                        WHEN instr(substr(url, 8), '/') > 0 THEN substr(url, 8, instr(substr(url, 8), '/') - 1)
                                        WHEN instr(substr(url, 8), '?') > 0 THEN substr(url, 8, instr(substr(url, 8), '?') - 1)
                                        ELSE substr(url, 8)
                                    END
                                WHEN url LIKE 'https://%' THEN 
                                    CASE 
                                        WHEN instr(substr(url, 9), '/') > 0 THEN substr(url, 9, instr(substr(url, 9), '/') - 1)
                                        WHEN instr(substr(url, 9), '?') > 0 THEN substr(url, 9, instr(substr(url, 9), '?') - 1)
                                        ELSE substr(url, 9)
                                    END
                                ELSE 
                                    CASE 
                                        WHEN instr(url, '/') > 0 THEN substr(url, 1, instr(url, '/') - 1)
                                        WHEN instr(url, '?') > 0 THEN substr(url, 1, instr(url, '?') - 1)
                                        ELSE url
                                    END
                            END as domain,
                            COUNT(*) as count
                            FROM links 
                            GROUP BY domain 
                            ORDER BY count DESC 
                            LIMIT 20'''):
        top_sites.append(row)

    c.close()

    return render_template('top.html',
                            top_sites=top_sites,
                            server=server,
                            channel=channel)
