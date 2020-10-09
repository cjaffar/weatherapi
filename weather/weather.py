import os, requests, sys, json

class Weather :

	def __init__(self, city = False) :  #, fromdate, todate=False) :
		self._city = city
		# self.fromdate = fromdate
		# self.todate = todate

	@property
	def city(self) :
		return self._city

	@property
	def location_path(self) :

		data_location = os.path.abspath( os.path.join( os.path.dirname(__file__), '..', 'data' ) )

		data_location_file = os.path.join( data_location, 'locations.json' )

		if not os.path.isfile( data_location_file ) : ### include some logic here to re-generate the location file.!???
			self.reset_locations(data_location_file)

		return data_location_file

	def index(self, base_url) :
		
		location = self.location_path

		result = []
		result.append( '%s%s' % (base_url, 'locations') )
		result.append( '%s%s/city' % (base_url, 'weather') )

		return result

	def get_city_key(self, city) :
		print(city, file=sys.stdout)
		data_location_file = self.location_path

		result = 0

		with open( data_location_file, 'r' ) as locations : #### preferably this can be done in a DB

			all_locations = json.load(locations)

			for loc in all_locations :

				for key, value in loc.items() :
					if key.lower() == city.lower() :
						return value.get('Key', 0)

		return result

	def get(self) :

		key = os.getenv("API_KEY")

		url = os.getenv("FORECASTS_URL")

		city = self.get_city_key( self.city )

		# print(city)
		url = "%s%s/%d?apikey=%s" % (url, '5day', int(city), key )
		# print(url, file=sys.stdout)

		result = { 'success': False }
		response = requests.get(url)

		if response.status_code == 200 :

			data = response.json()

			forecasts = data.get('DailyForecasts', [])
			num_forecasts = len(forecasts)

			temperature = []
			for temp in forecasts :

				daytemp = temp.get('Temperature', {})
				
				mintemp = daytemp.get('Minimum', {})
				maxtemp = daytemp.get('Maximum', {})

				temperature.append( maxtemp.get('Value', 0) - mintemp.get('Value', 0) )

			if temperature :
				result['success'] = True

				temperature.sort()

				result['min'] = min(temperature)
				result['max'] = max(temperature)
				result['average'] = sum(temperature) / num_forecasts
				result['median'] = temperature[ num_forecasts // 2 ]

		return result

	def write_locations(self, path) :

		url = os.getenv("LOCATIONS_URL")
		key = os.getenv("API_KEY")

		url = '%s%d?apikey=%s' % (url, 50, key ) ##supported values at accuweather is 50, 100, 150

		response = requests.get( url )

		if response.status_code == 200 :

			data = response.json()

			with open(data_location_file, 'w') as json_write :

				contents = []
				for d in data :

					contents.append( { d.get('EnglishName', 'N/A').lower() : d } )
				
				json.dump( contents, json_write )

			return True

		return False


	def get_locations(self) :

		data_location_file = self.location_path

		result = []

		with open( data_location_file, 'r' ) as locations : #### preferably this can be done in a DB

			all_locations = json.load(locations)

			for city in all_locations :
				
				for key, value in city.items() : ## for readability, otherwise list comprehension.
					result.append( { 'city' : value['EnglishName'], 'country' : value['Country']['EnglishName'], 'region' : value['Region']['EnglishName'] } )

		return result