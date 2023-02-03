from flask import Flask 
app = Flask(__name__)

@app.route('/')
def sport() : 
    return 'hi. this is the firts work in this project.'