from flask import Flask
app = Flask(__name__)

#@app.route("/")
#def hello():
#    return "Hello World!"
@app.route("/")
def goodbye():
    return "\n... and goodbye"

if __name__ == "__main__":
    app.run()
