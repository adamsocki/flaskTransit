from flask import Flask, render_template, abort
import requests
import gtfs_realtime_pb2 as gtfs_rt

app = Flask(__name__)

def fetch_realtime_data():
    # Fetch the data from the real-time API
    # This URL will depend on the specific API you're using
    url = 'http://example.com/path/to/realtime/api'
    response = requests.get(url)
    
    # Parse the response
    feed = gtfs_rt.FeedMessage()
    feed.ParseFromString(response.content)
    return feed

def get_vehicle_data(vehicle_id):
    feed = fetch_realtime_data()

    for entity in feed.entity:
        if entity.id == vehicle_id:
            return entity.vehicle

    # If the vehicle was not found in the feed, return None
    return None

@app.route('/bus_info/<bus_id>')
def show_bus_info(bus_id):
    # This function will be called whenever a user visits a URL that
    # matches the pattern '/bus_info/something'. The actual string that
    # appears in place of 'something' will be passed as 'bus_id'.
    return 'You asked for information about bus ' + bus_id

@app.route('/realtime/<vehicle_id>')
def realtime(vehicle_id):
    vehicle = get_vehicle_data(vehicle_id)
    if vehicle is None:
        abort(404, description="Vehicle not found")

    # Convert the vehicle data to a dict
    # Note that this code assumes that the VehiclePosition message contains
    # the fields 'latitude', 'longitude', and 'timestamp', and that the
    # VehicleDescriptor message contains the field 'id'.
    data = {
        'trip': {
            'trip_id': vehicle.trip.trip_id,
            'start_time': vehicle.trip.start_time,
            'start_date': vehicle.trip.start_date,
            'schedule_relationship': vehicle.trip.schedule_relationship,
            'route_id': vehicle.trip.route_id,
            'direction_id': vehicle.trip.direction_id,
        },
        'position': {
            'latitude': vehicle.position.latitude,
            'longitude': vehicle.position.longitude,
            'timestamp': vehicle.position.timestamp,
        },
        'vehicle': {
            'id': vehicle.vehicle.id,
            'occupancy_status': vehicle.occupancy_status,
            'multi_carriage_details': [
                {
                    'id': carriage.id,
                    'label': carriage.label,
                    'occupancy_status': carriage.occupancy_status,
                    'carriage_sequence': carriage.carriage_sequence,
                } for carriage in vehicle.multi_carriage_details
            ],
        },
    }

    # Render the bus_info.html template with the vehicle data
    return render_template('bus_info.html', bus_info=data)

if __name__ == '__main__':
    app.run(debug=True)
