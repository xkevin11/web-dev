import os

import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
	f = open('passengers.csv')
	reader = csv.reader(f)
	for name, flight_id in reader:
		db.execute("INSERT INTO airline.passengers (name, flight_id) VALUES (:name, :flight_id)", {"name": name, "flight_id": flight_id})
		print(f"Added passenger {name}'s flight ID={flight_id} into passengers table")
	db.commit()

if __name__ == "__main__":
	main()