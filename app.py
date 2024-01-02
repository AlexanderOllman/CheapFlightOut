from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
from ryanair import Ryanair
from ryanair.types import Flight
import json

api = Ryanair(currency="GBP")  # Euro currency, so could also be GBP etc. also
tomorrow = datetime.today().date() + timedelta(days=1)

# # Returns a list of Flight namedtuples
# flight: Flight = flights[0]
# print(flight)  # Flight(departureTime=datetime.datetime(2023, 3, 12, 17, 0), flightNumber='FR9717', price=31.99, currency='EUR' origin='DUB', originFull='Dublin, Ireland', destination='GOA', destinationFull='Genoa, Italy')
# print(flight.price)  # 9.78


app = Flask(__name__)



# Load airport datax
with open('airports.json', 'r') as file:
    airports = json.load(file)

date_selected = datetime.today()
origin = ""
destination = ""

def get_top_three_flights(date, origin):
    flight_array = []
    flights = api.get_cheapest_flights(origin, date, date + timedelta(days=1))
    for flight in flights[0:3]:
        origin_flag = [airport for airport in airports if flight.origin in airport['code']][0]
        dest_flag = [airport for airport in airports if flight.destination in airport['code']][0]
        booking_link = f"https://www.ryanair.com/gb/en/trip/flights/select?adults=1&teens=0&children=0&infants=0&dateOut={flight.departureTime.strftime('%Y-%m-%d')}&dateIn=&isConnectedFlight=false&discount=0&promoCode=&isReturn=false&originIata={flight.origin}&destinationIata={flight.destination}"
        single_flight = [flight.departureTime.strftime("%Y-%m-%d"),flight.departureTime.strftime("%H:%M"), flight.flightNumber, flight.price, flight.currency, flight.origin, flight.originFull, origin_flag['flag_link'], flight.destination, flight.destinationFull, dest_flag['flag_link'], booking_link]
        flight_array.append(single_flight)

    return flight_array

def get_flights_by_country(date, origin):
    flights = api.get_cheapest_flights(origin, date, date + timedelta(days=1))
    countries = []
    for flight in flights:
        print(flight.destination)
        origin = [airport for airport in airports if flight.origin in airport['code']][0]
        dest = [airport for airport in airports if flight.destination in airport['code']][0]

        print(dest['country'])

        if not any(country['destination'] == dest['country'] for country in countries):
            countries.append({'destination': dest['country'], 'price': flight.price})
        else:
            index = next(i for i, country in enumerate(countries) if country['destination'] == dest['country'])
            if countries[index]['price'] > flight.price:
                countries[index]['price'] = flight.price
        
        print(countries)

    print(countries)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update_date', methods=['POST'])
def update_date():
    global origin
    date = request.form['date']
    date_format = '%Y-%m-%d'
    today = datetime.strptime(date, date_format)

    if origin != "":
        get_flights_by_country(today, origin)
        flights = get_top_three_flights(today, origin)
    
    return jsonify({'date': date, 'flights': flights})



@app.route('/suggest_airports', methods=['GET'])
def suggest_airports():
    query = request.args.get('query', '').lower()
    # Filter airports based on the query
    cities = [airport for airport in airports if query in airport['city'].lower()]
    # countries = [airport for airport in airports if query in airport['country'].lower()]
    # Add countries for ideal destination search 
    suggestions = cities #+ countries
    return jsonify(suggestions)

@app.route('/select_airport', methods=['POST'])
def select_airport():
    global origin
    code = request.form['code']
    origin = code
    return jsonify({'code': code})

if __name__ == '__main__':
    app.run(debug=True)
