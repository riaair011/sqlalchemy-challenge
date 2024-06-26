# Import the dependencies.
import sqlalchemy
import datetime as dt
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlachemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect the tables
Base = automap_base()
Base.prepare(autoload_with=engine) 

# Save references to each table
measurement = Base.classes.measurement 

station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Availible Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    prcps= session.query(measurement.date, measurement.prcp).all()
    session.close()

    ##creating dictionary

    #Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.

#Return the JSON representation of your dictionary.


    prcps_val=[]
    data = session.query(measurement.date,measurement.prcp).\
    filter(measurement.date > '2016-08-22').all()
    for date, prcp in data:
        prcps_dic = {}
        prcps_dic["prcps"] = prcp
        prcps_dic["date"] = date
        prcps_val.append(prcps_dic)
        
    return jsonify(prcps_val)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stn= session.query(station.station).all()
    session.close()

    stns= list(stn)
    return jsonify(stns)

@app.route("/api/v1.0/tobs")
def tobs():
    #query dates and temperature of most active station for previous year of data and return a list 
    data = session.query(measurement.tobs).\
        filter(measurement.station=='USC00519281').\
        filter(measurement.date> '2016-08-17').all()
    temperature = list((np.ravel(data)))
    return jsonify(temperature= temperature)

@app.route("/api/v1.0/<start>")
def start(start):
    dt_tobs = session.query(function.min(measurement.tobs), function.max(measurement.tobs),function.avg(measurement.tobs).\
                            .filter(measurement.date>=date).all()
    dt_tobs_con= list(np.ravel(dt_tobs))
    return jsonify(dt_tob_con)

@app.route("/api/v1.0/start/end")
def startend(start,end):
    range_temps = session.query(function.min(measurement.tobs), function.max(measurement.tobs),function.avg(measurement.tobs).\
                            .filter(measurement.date>=date).filter(measurement.date<=end).all()
    range_temps_con = list(np.ravel(range_temps))
    return jsonify(range_temps_con)



if __name__ == '__main__':
    app.run(debug=True)
