from flask import Flask
app = Flask(__name__)

@app.route('/book/<uid>')
def book_by_uid(uid):
    return 'got %s' % uid
