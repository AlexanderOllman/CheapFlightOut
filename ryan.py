from datetime import datetime, timedelta
from ryanair import Ryanair
from ryanair.types import Flight

api = Ryanair(currency="EUR")  # Euro currency, so could also be GBP etc. also
tomorrow = datetime.today().date() + timedelta(days=1)
print(type(datetime.today().date()))
flights = api.get_cheapest_flights("DUB", tomorrow, tomorrow + timedelta(days=1))

# # Returns a list of Flight namedtuples
# flight: Flight = flights[0]
# print(flight)  # Flight(departureTime=datetime.datetime(2023, 3, 12, 17, 0), flightNumber='FR9717', price=31.99, currency='EUR' origin='DUB', originFull='Dublin, Ireland', destination='GOA', destinationFull='Genoa, Italy')
# print(flight.price)  # 9.78

print(flights[0:3])