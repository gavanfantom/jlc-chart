import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

import requests
import datetime
import time
import json

from .db import get_db

class fetcher:
    def __init__(self, base_url='https://jlcpcb.com/shoppingCart/smtGood/getComponentDetail?{}', query='componentLcscId={}', period=1, retries=5, retry_delay=30):
        self.base_url = base_url
        self.last_use = 0
        self.period = period
        self.retries = retries
        self.retry_delay = retry_delay
        self.query = query

    def fetch(self, component, base_url=None, query=None):
        if base_url is None:
            base_url = self.base_url
        if query is None:
            query = self.query
        trycount = self.retries
        while True:
            now = time.monotonic()
            while now - self.last_use < self.period:
                time.sleep(now - self.last_use)
                now = time.monotonic()
            self.last_use = now
            #print("Querying {}".format(base_url.format(query.format(component))))
            r = requests.get(base_url.format(query.format(component)))
            #print("Got status {}".format(r.status_code))
            if r.status_code == 200:
                return r.text
            if trycount > self.retries:
                return None
            trycount += 1
            time.sleep(self.retry_delay)

def get_fetcher():
    if 'f' not in g:
        g.f = fetcher()

    return g.f

def init_app(app):
    app.cli.add_command(poll_command)

@click.command('poll')
@with_appcontext
def poll_command():
    """Fetch data from JLCPCB."""
    db = get_db()
    f = get_fetcher()

    components = db.execute("""select id from fetchlist;""").fetchall()

    sqlite_insert_with_param = """INSERT INTO 'components' ('id', 'timestamp', 'data') VALUES(?, ?, ?);"""

    for (component,) in components:
        j = f.fetch(component)
        timestamp = datetime.datetime.now()
        if j:
            data = (component, timestamp, j)
            db.execute(sqlite_insert_with_param, data)
            db.commit()
        else:
            click.echo("Failed to fetch component {}".format(component))

    click.echo("Polling complete")

