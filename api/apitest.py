import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/',methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototoype API.</p>"

app.run(host = '0.0.0.0', port = 8080)