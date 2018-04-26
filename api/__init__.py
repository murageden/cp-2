from flask import Flask

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'p9Bv<3Eid9%$i01'

@app.route('/')
def hello_world():
	return "Hello wonderful world"