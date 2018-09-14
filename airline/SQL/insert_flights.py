import os

import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
	f = open('flights.csv')
	reader = csv.reader(f)
	for origin, destination, duration in reader:
		db.execute("INSERT INTO airline.flights (origin, destination, duration) VALUES (:origin, :destination, :duration)", {"origin": origin, "destination": destination, "duration": duration})
		print(f"Added {origin} to {destination} into flights table")
	db.commit()

if __name__ == "__main__":
	main()