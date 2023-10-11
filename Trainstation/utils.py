
from geopy.distance import geodesic
from math import ceil

def calculate_distance_and_time(station1, station2,train_speed):
    # Assuming station1 and station2 have latitude and longitude attributes
    coords1 = (station1.lattitue, station1.longitude)
    coords2 = (station2.lattitue, station2.longitude)
    distance = geodesic(coords1, coords2).kilometers  # Calculate distance in kilometers
    # Calculate predicted time based on the distance and train speed
    predicted_time = (distance / train_speed )*60  # Adjust train_speed as needed
    return ceil(distance), predicted_time
