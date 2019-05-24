import numpy as np
import pandas as pd
import datetime as dt
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)
from flask import Flask, jsonify
app = Flask(__name__)
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
    f"Available Routes:<br/>"
    f"/api/v1.0/percipitation"
    f"/api/v1.0/stations"
    f"/api/v1.0/tobs"
    f"/api/v1.0/<start>"
    f"/api/v1.0/<start>/<end>" 
     )

@app.route("/api/v1.0/percipitation")
def percipitation():
    """Return a list of all percipitation"""
    # Query all percipitation
    results = session.query(Measurement.prcp).all()

    # Convert list of tuples into normal list
    all_percipitation = list(np.ravel(results))

    return jsonify(all_percipitation)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations"""
    # Query all stations
    results = session.query(Station.name, Station.station).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of all tempature observations"""
    # Query all temperatures
    results = session.query(Measurement.tobs).all()

    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start(start_date):
    ""
    # When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than 
    #and equal to the start date
    sel = [func.min(Measurement.tobs),
           func.max(Measurement.tobs),
           func.avg(Measurement.tobs)]
                
    results = session.query(*sel).filter(Measurement.date >= start_date).all()
    tmps = list(np.ravel(results))
    
    return jsonify(tmps)
    
    
    
@app.route("/api/v1.0/<start>/<end>")
def start_end(start_date, end_date):

    #When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates 
    #between the start and end date inclusive.  
    
    sel = [func.min(Measurement.tobs),
           func.max(Measurement.tobs),
           func.avg(Measurement.tobs)]
    
    results = session.query(*sel).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    tmps = list(np.ravel(results))
    
    return jsonify(tmps)
    
    
    
if __name__ == '__main__':
    app.run(debug=True)