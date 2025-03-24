import sqlite3
from datetime import datetime

import click
from flask import current_app, g

def get_db():
    if 'db' not in g: # Start database connection if there isn't already one
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row # tells the connection to return row that can be accessed like dicts, where the columns names are the keys.
    return g.db

def close_db(e=None): # Close the database connection by checking if a connection is inside of g
    db = g.pop('db', None)

    if db is not None: # database connection was set, so we close it
        db.close()

def init_db():
    db = get_db() # Starts a database connection needed to execute SQL commands

    with current_app.open_resource('schema.sql') as f: # run the database schema so the tables are created using our 'db' database connection
        db.executescript(f.read().decode('utf-8'))

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialised the database.')

sqlite3.register_converter( # Telling python how to handle timestamp values in our database by converting them to datetime.datetime
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

def init_app(app):
    app.teardown_appcontext(close_db) # Tells flask to call the given function after getting a response
    app.cli.add_command(init_db_command) # Adds the command to the CLI that can be called with the 'flask' command