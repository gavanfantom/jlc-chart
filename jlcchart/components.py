from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

import json

from .db import get_db

bp = Blueprint('components', __name__, url_prefix='/components')


@bp.route('<list:components>')
def components(components):
    db = get_db()
    results = []
    for component in components:
        rows = db.execute("""SELECT timestamp, json_extract(data, '$.data.stockCount') AS stock FROM components WHERE id=? ORDER BY timestamp;""", (component,)).fetchall()
#        if not rows:
#            abort(404, f"Component {component} doesn't exist.")

        data = []
        for row in rows:
            data.append({'timestamp' : row['timestamp'], 'value' : row['stock']})

        row = db.execute("""SELECT timestamp, data FROM components WHERE id=? ORDER BY timestamp DESC LIMIT 1;""", (component,)).fetchone()

        #if row is None:
        #    abort(404, f"Error retrieving component {component}.")

        try:
            details = json.loads(row['data'])
            code = details['data']['componentCode']
            name = details['data']['componentName']
        except:
            code = component 
            name = "Not Found"
        results.append({'data': data, 'id': component, 'code': code, 'name': name})

    return render_template('component.html', components=results)

