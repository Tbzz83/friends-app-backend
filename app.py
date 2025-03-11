# TODO: UPDATE THIS FILE FOR DEPLOYMENT
from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import dotenv_values
import os
import sys

# GLOBALS 
CONFIG = dotenv_values(".env")

# Check if CONFIG file exists
if not CONFIG:
  print(".env doesn't exist. Creating...")

  # IF CONFIG doesn't exist, create a map and use os.getenv() to pull
  # environment variables. 
  CONFIG = {
    "sql_host_db" : os.getenv("SQL_HOST_DB"),
    "sql_pw" : os.getenv("SQL_PW"),
    "sql_user" : os.getenv("SQL_USER")}

  # If it STILL doesn't exist, exit.
  for values in CONFIG.values():
    if not values:
      print("No matching environment variables found.")
      sys.exit(1)

app = Flask(__name__)

CORS(app) 

# >>> SQL DB setup >>>

# Must quote password if it has special characters
sql_pw = quote(CONFIG["sql_pw"])

# If using Azure SQL DB connection string sql_host_db will look like:
sql_host_db = CONFIG["sql_host_db"]
sql_user = CONFIG["sql_user"]
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{sql_user}:{sql_pw}@{sql_host_db}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# <<< SQL DB setup <<<

#frontend_folder = os.path.join(os.getcwd(),"..","frontend")
#dist_folder = os.path.join(frontend_folder,"dist")

# Server static files from the "dist" folder under the "frontend" directory
#@app.route("/",defaults={"filename":""})
#@app.route("/<path:filename>")
#def index(filename):
#  if not filename:
#    filename = "index.html"
#  return send_from_directory(dist_folder,filename)

# api routes
import routes

with app.app_context():
  db.create_all()


  


if __name__ == "__main__":
  host = os.getenv("FLASK_RUN_HOST", "0.0.0.0")
  port = int(os.getenv("FLASK_RUN_PORT", 5000))

  app.run(debug=True, host=host, port=port)
