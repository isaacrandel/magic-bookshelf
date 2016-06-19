FLASK_APP=web.py

run:
	FLASK_APP=$(FLASK_APP) flask run

make-db:
	sqlite3 db/magicbookshelf.db < db/magicbookshelf.schema
