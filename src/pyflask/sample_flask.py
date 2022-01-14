# sample_flask.py
# an object of WSGI application
from flask import Flask	
app = Flask(__name__) # Flask constructor

# A decorator used to tell the application
# which URL is associated function
@app.route('/')	
def hello():
	return "HELLO WORLD!"

# routing the decorator function hello_name
# localhost:5000/hello/flask
@app.route('/hello/<name>')  
def hello_name(name):
   return f'Hello {name}!'

if __name__=='__main__':
    # default points to localhost:5000
    app.run()

    # host='0.0.0.0' indicates use the ipaddress of the current OS instance where this
    # app is running.
    # In windows you can use ipconfig get the ipaddress from 'IPv4 Address'
    # linux use ifconfig -a
    # app.run(debug=True,host='0.0.0.0', port=5000)

    # points to localhost:8080
    # app.run( port=8080)