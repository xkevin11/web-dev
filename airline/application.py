# To Run:	
# 	export FLASK_APP=application.py
# 	flask run

import os

from flask import Flask, render_template, request

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)

engine = create_engine(os.getenv("DATABASE_URL")) 
db = scoped_session(sessionmaker(bind=engine))


@app.route('/')
def index():
    flights = db.execute("SELECT * FROM airline.flights").fetchall()
    return render_template('index.html', flights=flights)


@app.route('/book', methods=["POST"])
def book():
	"""Book flight."""
	name = request.form.get("name")

    # make sure flight_id is integer
	try:
		flight_id = int(request.form.get("flight_id"))
	except ValueError:
		return render_template("error.html", message="Invalid flight number")

    # make sure flight_id exists
	if db.execute("SELECT * FROM airline.flights WHERE id = :id", {'id':flight_id}).rowcount ==0:
		return render_template("error.html", message="No such flight with that id.")
    
	db.execute("INSERT INTO airline.passengers (name, flight_id) VALUES (:name, :flight_id)", {"name": name, "flight_id": flight_id})
	db.commit()
	return render_template("success.html", name=name)



@app.route('/flights')
def flights():
	"""Lists all flights."""
	flights = db.execute("SELECT * FROM airline.flights").fetchall()
	return render_template('flights.html', flights=flights)


@app.route('/flight/<int:flight_id>')
def flight(flight_id):
	"""Lists detailes about a single flight."""

	# make sure flight_id exists
	flight = db.execute("SELECT * FROM airline.flights WHERE id = :id", {'id':flight_id}).fetchone()
	if flight is None:
		return render_template("error.html", message="No such flight.")

    # get all passengers.
	passengers = db.execute("SELECT name FROM airline.passengers where flight_id = :flight_id", {'flight_id':flight_id}).fetchall()
	return render_template('flight.html', flight=flight, passengers=passengers)





