from flask import Flask
from backend.models import *

app=None

def init_app():
    tapp=Flask(__name__)
    tapp.debug=True
    tapp.secret_key="22f1000091"
    tapp.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///IESCP.sqlite3"
    tapp.app_context().push()
    db.init_app(tapp)
    db.create_all()
    print("IESCP application started....")
    return tapp

app=init_app()
from backend.controls import *

if __name__=="__main__":
    app.run()