# jlc-chart

Flask app to chart component stock levels from JLCPCB

# Installation

This app can be deployed in the same way as any other WSGI application.

With Apache, that looks something like this:

    WSGIDaemonProcess jlc-chart user=... group=... threads=2
    WSGIScriptAlias /jlc-chart /path/to/jlc-chart/wsgi.py
    WSGIScriptReloading On

    <Directory /path/to/jlc-chart>
        WSGIProcessGroup jlc-chart
        WSGIApplicationGroup %{GLOBAL}
        AuthType Basic
        AuthName "Restricted Content"
        AuthUserFile /path/to/.htpasswd
        Require valid-user
    </Directory>

Once configuration is complete, the database must be initialised:

    flask init-db

Once up and running, a cron job must be created to perform the poll:

    crontab -e
    1   9       *       *       *       /path/to/jlc-chart/poll

# Acknowledgements

With thanks to Unipart Digital for graciously allowing me to retain copyright
of this project after it was initially developed as an in-house tool.

