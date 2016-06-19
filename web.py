import os

from flask import (
    abort,
    Flask,
    jsonify,
    request,
    send_from_directory
)

import store


app = Flask(__name__)


@app.route('/')
def root():
    root_dir = os.getcwd()
    static_dir = os.path.join(root_dir, 'frontend')
    return send_from_directory(static_dir, 'index.html')


@app.route('/book/')
def book_by_uid_or_title():
    uid = request.args.get('uid')
    title = request.args.get('title')

    if uid:
        book = store.retrieve_book_by_uid(uid)
    elif title:
        book = store.retrieve_book_by_title(title)
    else:
        abort(400)

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
