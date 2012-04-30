from flask import Flask

app = Flask(__name__)
#app.config.from_object(__name__)

@app.route('/')
def index():
#  return render_template('index.html', message = range(0, 10000))
  return "\n... this is index"

if __name__ == '__main__':
  app.run(host = '127.0.0.1')
#  app.run()
