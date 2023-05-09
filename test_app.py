import unittest
from unittest.mock import patch
from app.py import app  # replace 'your_flask_app_file' with the actual name of your Flask application file
import gtfs_realtime_pb2 as gtfs_rt

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

    @patch('app.fetch_realtime_data')  # replace 'your_flask_app_file' with the actual name of your Flask application file
    def test_realtime_route(self, mock_fetch):
        # Mocking the function to return a fixed set of data
        mock_vehicle = gtfs_rt.FeedEntity()
        mock_vehicle.id = '1'
        mock_vehicle.vehicle.trip.trip_id = 'trip1'
        mock_vehicle.vehicle.trip.start_time = '14:05:00'
        mock_vehicle.vehicle.trip.start_date = '20220628'
        mock_vehicle.vehicle.trip.schedule_relationship = 0
        mock_vehicle.vehicle.trip.route_id = 'ROUTE1'
        mock_vehicle.vehicle.trip.direction_id = 0
        mock_vehicle.vehicle.position.latitude = 123.45
        mock_vehicle.vehicle.position.longitude = 12.345
        mock_vehicle.vehicle.position.timestamp = 1656390815
        mock_vehicle.vehicle.vehicle.id = 'vehicle1'
        mock_vehicle.vehicle.occupancy_status = 0

        mock_feed = gtfs_rt.FeedMessage()
        mock_feed.entity.extend([mock_vehicle])
        mock_fetch.return_value = mock_feed

        # Call the /realtime/<vehicle_id> route with the mocked data
        response = self.client.get('/realtime/1')
        self.assertEqual(response.status_code, 200)

        # Call the /bus_info/<bus_id> route
        response = self.client.get('/bus_info/1')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
