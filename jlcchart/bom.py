from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)

from werkzeug.exceptions import abort

import json
import csv
import re
import io

from .db import get_db
from .fetcher import get_fetcher

bp = Blueprint('bom', __name__, url_prefix='/bom')

def match(x):
    m = re.search("C\d+", x)
    if m:
        return m.group()
    else:
        return None

@bp.route('/add', methods=(['POST']))
def add():
    db = get_db()
    f = get_fetcher()

    if request.method == 'POST':
        component = request.json['code']

        row = db.execute("""SELECT id FROM fetchlist WHERE code = ?""", (component,)).fetchone()
        if row is not None:
            return jsonify(id=row[0])

        j = f.fetch(component, base_url='https://cart.jlcpcb.com/shoppingCart/smtGood/getComponentDetail?{}', query='componentCode={}')
        if j:
            try:
                j = json.loads(j)
                lcsc_id = j['data']['lcscComponentId']
            except:
                abort(404, "Component {} not found".format(component))
            db.execute("""INSERT INTO 'fetchlist' ('id', 'code') VALUES(?, ?);""", (lcsc_id, component))
            db.commit()
            return jsonify(id=lcsc_id)
        else:
            abort(404, "Component {} not found".format(component))

@bp.route('/', methods=('GET', 'POST'))
def bom():
    db = get_db()

    bom = []
    if request.method == 'POST':
        stream = io.StringIO(request.form['bom'])
        r = csv.reader(stream)
        for row in r:
            bom.append(row)
        maxlen = max(len(i) for i in bom)
        for row in bom:
            if len(row) < maxlen:
                row.extend('' for _ in range(maxlen - len(row)))
        if len(bom) < 1:
            abort(400, "No BOM supplied")
        has_header = True
        for val in bom[0]:
            if match(val):
                has_header = False
        if has_header:
            header = bom[0]
            bom = bom[1:]
        else:
            header = ['' for _ in range(maxlen)]
        bom_col = list(zip(*bom))
        count = []
        for column in bom_col:
            total = 0
            for x in column:
                if match(x):
                    total += 1
            count.append(total)
        componentcol = None
        for i, val in enumerate(count):
            if val == max(count):
                componentcol = i
                break

        if max(count) < 1:
            abort(400, "BOM must contain at least one component")
        components = [match(x) for x in bom_col[componentcol]]

        ids = []
        for component in components:
            row = db.execute('SELECT id from fetchlist WHERE code=?', (component,)).fetchone()
            if row:
                ids.append(row[0])
            else:
                ids.append('')

        header += ['JLC code', 'JLC ID']
        table_col = bom_col + [components] + [ids]
        table = list(zip(*table_col))

        return render_template('bom.html', headings=header, table=table)
    return render_template('bom_form.html')

