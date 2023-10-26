from PIL import Image, ImageDraw, ImageFont

from geopy.distance import geodesic
from math import ceil
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

def calculate_distance_and_time(station1, station2,train_speed):
    # Assuming station1 and station2 have latitude and longitude attributes
    coords1 = (station1.lattitue, station1.longitude)
    coords2 = (station2.lattitue, station2.longitude)
    distance = geodesic(coords1, coords2).kilometers  # Calculate distance in kilometers
    # Calculate predicted time based on the distance and train speed
    predicted_time = (distance / train_speed )*60  # Adjust train_speed as needed
    return ceil(distance), predicted_time

def calculate_ticket_price(base_fare, distance, additional_charges, seat_reservation_fee=0, discount=0):
    # Calculate the fare based on the distance
    distance_fare = distance * 0.20

    # Calculate the total fare without discount
    total_fare = base_fare + distance_fare + seat_reservation_fee + additional_charges

    # Calculate the discount amount
    discount_amount = (total_fare * discount) / 100

    # Apply the discount to the total fare
    discounted_fare = total_fare - discount_amount

    print(total_fare,discount_amount,discounted_fare)

    return total_fare , discounted_fare , discount_amount

 



def create_image_from_model(ticket_booking):
    # Create a blank image with a white background
    width, height = 800, 400
    image = Image.new('RGB', (width, height), 'white')

    # Initialize the drawing context
    draw = ImageDraw.Draw(image)

    # Define the custom font and size
    font_path = "F:\\railway management system\\railway\\static\\fonts\\ABeeZee-Regular.otf"  # Replace with the path to your custom font file
    custom_font = ImageFont.truetype(font_path, size=16)

    # Position and format the title
    title_text = "Ticket Information"
    title_x, title_y = 20, 20
    title_color = 'black'
    draw.text((title_x, title_y), title_text, fill=title_color, font=custom_font)

    # Extract fields from the model object
    name = ticket_booking.name
    email = ticket_booking.email
    from_station_name = ticket_booking.from_station.name
    to_station_name = ticket_booking.to_station.name
    event_date = ticket_booking.event_date
    total_price = ticket_booking.total_price
    reservation = ticket_booking.reservation
    reservation_seat = ticket_booking.reservation_seat
    ticket_number = ticket_booking.id
    train_number = ticket_booking.route.train.train_id
    train_name = ticket_booking.route.train.name
    discount = ticket_booking.discount

    # Position and format the model data
    data_x, data_y = 20, 60
    data_color = 'black'
    line_height = 20

    model_data = {
        "Name": name,
        "Email": email,
        'From Station': from_station_name,
        'To Station': to_station_name,
        "Train Name": train_name,
        "Train Number": train_number,
        "Reservation": reservation,
        "Reservation Seat No": reservation_seat,
        'Event Date': event_date,
        'Ticket Number': ticket_number,
        'discount':str(discount) +  "% govt approved privilage" if discount>0 else 0,
        
        'Total Price': total_price,
        'discounted price': ceil(total_price - (total_price*discount)/100) if discount>0 else 0
    }

    for field, value in model_data.items():
        line = f"{field}: {value}"
        draw.text((data_x, data_y), line, fill=data_color, font=custom_font)
        data_y += line_height

    img_byte_array = BytesIO()
    image.save(img_byte_array, format='PNG')
    img_file = InMemoryUploadedFile(
        img_byte_array,
        None,
        'ticket.png',
        'image/png',
        img_byte_array.tell(),
        None
    )

    # Save the image to the model field
    ticket_booking.ticket_image = img_file
    ticket_booking.save()