FLASK_APP=web.py
DB=db/magicbookshelf.db

run:
	FLASK_APP=$(FLASK_APP) flask run --host=0.0.0.0

schema:
	rm $(DB)	
	sqlite3 $(DB) < db/magicbookshelf.schema
