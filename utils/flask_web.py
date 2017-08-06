from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/')
def hello_world():
	print 'User-Agent: ', request.headers.get('User-Agent')
	print 'remote_addr:', request.remote_addr
	return 'Hello World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
