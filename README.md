# magic-bookshelf

The code in this repository is for my Magic Bookshelf (https://youtu.be/RsUnRipk-qs), an RFID enabled bookshelf system powered by python and a raspberry pi.

## Setup
```
pip install -r requirements.txt
make schema
```

There's no interface for adding books to the database, but you can add them using `store.store_book` in a python shell.

## Running the controller

`make run-controller`

## Running the web app

`make run-web`
