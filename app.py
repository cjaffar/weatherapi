from flask import Flask, request
# from flask_restful import Resource, Api
from dotenv import load_dotenv

from weather.weather import Weather

app = Flask(__name__)
# api = Api(app)

@app.route('/')
def index() :
	w = Weather()
	result = w.index(request.base_url)
	return { 'items' : result }

@app.route('/weather/<city>')
def get(city) :
	w = Weather( city )  #'Dhaka', '2020-10-20', '2020-10-30')
	result = w.get()
	return { 'success' : result.get('success', False), 'items' : result }

@app.route('/locations')
def locations() :
	w = Weather()
	result = w.get_locations()

	return { 'success' : True if result else False, 'items' : result  }


if __name__ == '__main__':

	
	load_dotenv()
	app.run(debug=True)
