''' Homework 11

- Due on Wednesday, April 16 by midnight by online submission through turnin.
- Leave the name of the file unchanged (hw11.py), and submit this file only.
- You *will* be graded on style.
- You may discuss problems with others, but write up the solutions yourself.

You will be building a simple to-do list app, because there simply aren't enough
of these.

Your database should be stored in a file called data.db file. You'll have to
initialize the database using a schema.sql file, as discussed in class.
You don't need to submit these files, though.

The database should contain one table with two columns: one for the to-do list
item id, and one for the to-do list text. The former should have the type
'integer primary key' and the name 'id'; the latter should have the type 'text'
and the name 'item.'
'''

from flask import *
import sqlite3
import requests
DATABASE = 'data.db'

app = Flask(__name__)
@app.route('/')
def get_items():
    ''' Return a list of current to-do items.

    The response should be JSON of the following format:
    { "results": [list of items] }

    Each item in the list should be a *dictionary* with fields
    'id' and 'item'. e.g.
    { "results": [ {"id": 1, "item": do laundry} ]}
    
    To do this, you'll probably want to use the description attribute of the cursor object,
    as discsussed in class.
    See here: https://docs.python.org/2/library/sqlite3.html#sqlite3.Cursor.description

    There are other options as well (namely row factories), see e.g.
    http://flask.pocoo.org/docs/patterns/sqlite3/#easy-querying

    By default, the results should be ordered by their primary key. But you should also
    support an optional GET request parameter "order", and if the value of this parameter
    is "alpha", then results should be in alphabetical order of the text field instead.
    '''
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    entry_id = request.args.get('order')
    if entry_id == 'alpha':
        results = c.execute('select * from entries order by item')
    else:
        results = c.execute('select * from entries order by id')
    results = results.fetchall()
    columns = c.description
    conn.close()
    keys = [key[0] for key in columns]
    return jsonify(results = [dict(zip(keys, value)) for value in results])

@app.route('/add', methods=['POST'])
def add_items():
    '''A POST-only endpoint. Accept POST data of the form:
    { "items": [ list of to-do items ] }

    Each item in the list will just be a string of text. You should
    add each one to the database. Return a JSON response of the form:
    { "response": "success" }
    '''
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    item = json.loads(request.form['items'])
    for kv in item:
        c.execute('insert into entries (id, item) values (?, ?)', (kv['id'], kv['item']))
    conn.commit()
    conn.close()
    return jsonify(response='success')

@app.route('/delete', methods=['POST'])
def delete_items():
    '''A POST-only endpoint. Accept POST data of the form:
    { "ids": [ list of to-do item ids ] }

    Each item in the list will just be an integer id. You should delete
    all to do items corresponding to those ids. If an invalid id is given,
    just ignore it. Return a JSON response of the form:
    { "response": "success" }
    '''
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    ids = json.loads(request.form['ids'])
    for key in ids:
        c.execute('delete from entries where id = ?', (key,))
    conn.commit()
    conn.close()
    return jsonify(response='success')


@app.route('/update', methods=['POST'])
def update_item():
    '''A POST-only endpoint. Accept POST data of the form:
    { "id": to-do item id, "item": to-do item text }
    You should update the current to-do item corresponding to the given id
    to have the new text. If an invalid id is given, just ignore it.

    *Instead* of returning { "response: "success" }, redirect the user back
    to the get_items endpoint. So the response should return the updated
    to-do list in JSON form. Take a look at the redirect and url_for functions
    provided by Flask.
    '''
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    ids = request.form['id']
    item = request.form['item']
    c.execute('update entries set item=? where id=?', (item, ids))
    conn.commit()
    conn.close()
    return redirect('http://127.0.0.1:5000/')


if __name__ == '__main__':
    app.run(debug=True)



