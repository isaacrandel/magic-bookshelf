import os

from flask import (
    abort,
    Flask,
    jsonify,
    send_from_directory
)

import store


app = Flask(__name__)


@app.route('/')
def root():
    root_dir = os.getcwd()
    static_dir = os.path.join(root_dir, 'frontend')
    return send_from_directory(static_dir, 'index.html')


@app.route('/book/<uid>')
def book_by_uid(uid):
    book = store.retrieve_book_by_uid(uid)
    if book:
        return jsonify(**book)
    else:
        abort(404)


@app.route('/checkin/<uid>')
def checkin_book(uid):
    book = store.retrieve_book_by_uid(uid)
    if book:
        book = store.checkin(book)
        return jsonify(**book)
    else:
        abort(404)


@app.route('/checkout/<uid>')
def checkout_book(uid):
    book = store.retrieve_book_by_uid(uid)
    if book:
        book = store.checkout(book)
        return jsonify(**book)
    else:
        abort(404)
