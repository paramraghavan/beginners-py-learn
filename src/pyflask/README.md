# What is Flask?
Flask is a Web-Application Framework or Web Framework. Flask’s framework is 
easier to learn than other frameworks like Django’s etc... It has less base code to
implement a simple web-Application. Flask is the collection of modules and libraries that
helps the developer to write applications without writing the low-level codes such as protocols,
thread management, etc. Flask is based on WSGI(Web Server Gateway Interface) toolkit and
Jinja2 template engine. 
>Note: Python 2.6 or higher is required for the installation of the Flask

## Sample Code 'Hello World!'
<pre>
# sample_flask.py
# an object of WSGI application
from flask import Flask	
app = Flask(__name__) # Flask constructor

# A decorator used to tell the application
# which URL is associated function
# localhost:5000
@app.route('/')	
def hello():
	return '<html><body><span style="background-color:#FF5733 ;"><b>HELLO WORLD!</b></span></body></html>'


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
</pre>

- copy the above code to sample_flask.py
- virtualenv venv - creates a virtual env under folder
- venv\Scripts\activate - activates virtualenv
- pip install flask
- Following packages are installed when flask is installed
<pre>
 Package      Version
 ------------ -------
 click        8.0.3
 colorama     0.4.4
 Flask        2.0.2
 itsdangerous 2.0.1
 Jinja2       3.0.3
 MarkupSafe   2.0.1
 Werkzeug     2.0.2
</pre>
- python sample_flask.py
- on browser localhost:5000
- on browser localhost:5000/hello/flask

## Reference/Interesting Articles:
- https://www.geeksforgeeks.org/python-introduction-to-web-development-using-flask/
- https://towardsdatascience.com/build-interactive-charts-using-flask-and-d3-js-70f715a76f93
- https://github.com/samirsaci/matrix-miserables/blob/master/static/js/matrix.js



