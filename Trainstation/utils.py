from geopy.distance import geodesic

def calculate_distance_and_time(station1, station2,train_speed):
    # Assuming station1 and station2 have latitude and longitude attributes
    coords1 = (station1.latitude, station1.longitude)
    coords2 = (station2.latitude, station2.longitude)
    distance = geodesic(coords1, coords2).miles  # Calculate distance in miles
    # Calculate predicted time based on the distance and train speed
    predicted_time = distance / train_speed  # Adjust train_speed as needed
    return distance, predicted_time
