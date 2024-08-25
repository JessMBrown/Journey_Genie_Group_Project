import unittest
from activities_api import OpenTripMapApi
from config import activities_api_key


class TestGetCoordinatesFunction(unittest.TestCase):

    def setUp(self):
        self.pass_api_key = OpenTripMapApi(activities_api_key)

    def test_coordinates_valid_London(self):
        self.expected = {
            "name": "london",
            "country": "GB",
            "lat": 51.50853,
            "lon": -0.12574,
            "population": 7556900,
            "timezone": "Europe/London",
            "status": "OK"
        }
        self.assertEqual(self.expected, OpenTripMapApi.get_coordinates(self.pass_api_key, "London"))

    def test_coordinates_valid_Tokyo(self):
        self.expected = {
            "name": "Tokyo",
            "country": "JP",
            "lat": 35.6895,
            "lon": 139.69171,
            "population": 8336599,
            "timezone": "Asia/Tokyo",
            "status": "OK"
        }
        self.assertEqual(self.expected, OpenTripMapApi.get_coordinates(self.pass_api_key, "Tokyo"))

        # NOTE: running the test module will have the below test fail due to an API constraints,
        # they do pass in isolation
    def test_coordinates_invalid_minus_51_point_223_and_100_point_100(self):
        self.expected = {'status': 'NOT_FOUND', 'error': 'Name -51.223, 100.100 at  not found'}
        self.assertEqual(self.expected, OpenTripMapApi.get_coordinates(self.pass_api_key, "-51.223, 100.100"))

    def test_coordinates_invalid_sefwr4356yth(self):
        self.expected = {'status': 'NOT_FOUND', 'error': 'Name sefwr4356yth at  not found'}
        self.assertEqual(self.expected, OpenTripMapApi.get_coordinates(self.pass_api_key, "sefwr4356yth"))

    def test_coordinates_invalid_empty(self):
        self.expected = None
        self.assertEqual(self.expected, OpenTripMapApi.get_coordinates(self.pass_api_key, ""))

    def test_coordinates_boundary_long_city_name(self):
        self.expected = {
            "name": "Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch",
            "country": "GB",
            "lat": 53.22141,
            "lon": -4.20329,
            "population": 3107,
            "timezone": "Europe/London",
            "status": "OK"
        }
        self.assertEqual(self.expected, OpenTripMapApi.get_coordinates(self.pass_api_key,
                                                                       "Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch"))

    def test_coordinates_boundary_shortest_city_name(self):
        self.expected = {
            "name": "A",
            "country": "NO",
            "lat": 63.96068,
            "lon": 10.22468,
            "population": 1145,
            "timezone": "Europe/Oslo",
            "status": "OK"
        }
        self.assertEqual(self.expected, OpenTripMapApi.get_coordinates(self.pass_api_key, "A"))


class TestGetActivitiesFunction(unittest.TestCase):

    def setUp(self):
        self.pass_api_key = OpenTripMapApi(activities_api_key)

    def test_activities_valid_London_51_point_50853_minus_0_point_12574_churches(self):
        self.expected = [
            {
                "name": "The Chinese Church in London",
                "kinds": "religion,churches,interesting_places,other_churches",
                "rate": 3,
                "xid": "W96237054"
            },
            {
                "name": "French Protestant Church of London",
                "kinds": "religion,churches,interesting_places,other_churches",
                "rate": 7,
                "xid": "W58645388"
            },
            {
                "name": "Welsh Church of Central London",
                "kinds": "religion,churches,interesting_places,other_churches",
                "rate": 7,
                "xid": "N4118984890"
            },
            {
                "name": "St Alphege London Wall",
                "kinds": "religion,churches,interesting_places,other_churches",
                "rate": 7,
                "xid": "Q7592313"
            },
            {
                "name": "St Swithin, London Stone",
                "kinds": "religion,churches,interesting_places,other_churches",
                "rate": 3,
                "xid": "Q7595498"
            },
            {
                "kinds": "religion,churches,interesting_places,other_churches",
                "name": "St Peter's London Docks",
                "rate": 7,
                "xid": "W361411779",
            },
            {
                "name": "London England Temple",
                "kinds": "religion,churches,interesting_places,other_churches",
                "rate": 3,
                "xid": "W186367197"
            }]
        self.assertEqual(self.expected,
                         OpenTripMapApi.get_activities(self.pass_api_key, "London", "51.50853", "-0.12574",
                                                       "churches"))

    # this endpoint only accepts names with a min of three or more chars, the previous /geoname accepts a minimum of one
    def test_activities_invalid_city_name_Lo(self):
        self.expected = None
        self.assertEqual(self.expected,
                         OpenTripMapApi.get_activities(self.pass_api_key, "Lo", "51.50853", "-0.12574",
                                                       "churches", 10000, 3))

    def test_activities_invalid_lat_1000(self):
        self.expected = None
        self.assertEqual(self.expected,
                         OpenTripMapApi.get_activities(self.pass_api_key, "London", "1000", "-0.12574",
                                                       "churches", 10000, 3))

    def test_activities_invalid_lon_1000(self):
        self.expected = None
        self.assertEqual(self.expected,
                         OpenTripMapApi.get_activities(self.pass_api_key, "London", "51.50853", "1000",
                                                       "churches", 10000, 3))

    def test_activities_invalid_kinds_none(self):
        self.expected = None
        self.assertEqual(self.expected,
                         OpenTripMapApi.get_activities(self.pass_api_key, "London", "51.50853", "1000", ""))


class TestGetActivityDetailsFunction(unittest.TestCase):

    def setUp(self):
        self.pass_api_key = OpenTripMapApi(activities_api_key)

    def test_xid_valid_Q17663855(self):
        self.expected = {
            "xid": "Q17663855",
            "name": "London Wall: the west gate of Cripplegate fort and a section of Roman wall in London Wall underground car park, adjacent to Nobl",
            "address": {
                "city": "City of London",
                "road": "London Wall",
                "state": "England",
                "county": "London",
                "suburb": "Temple",
                "country": "United Kingdom",
                "postcode": "EC2Y 5AP",
                "country_code": "gb",
                "house_number": "23",
                "state_district": "Greater London"
            },
            "rate": "1h",
            "wikidata": "Q17663855",
            "kinds": "defensive_walls,historic,fortifications,interesting_places",
            "sources": {
                "geometry": "wikidata",
                "attributes": [
                    "wikidata"
                ]
            },
            "otm": "https://opentripmap.com/en/card/Q17663855",
            "point": {
                "lon": -0.095414899289608,
                "lat": 51.51750183105469
            }
        }
        self.assertEqual(self.expected, OpenTripMapApi.get_activity_details(self.pass_api_key, "Q17663855"))

    def test_xid_invalid_17663855Q(self):
        self.expected = None
        self.assertEqual(self.expected, OpenTripMapApi.get_activity_details(self.pass_api_key, "17663855Q"))

    def test_xid_boundary_small_Q60308(self):
        self.expected = {
            "xid": "Q60308",
            "name": "London Wall",
            "address": {
                "city": "City of London",
                "road": "London Wall",
                "house": "Museum of London",
                "state": "England",
                "county": "London",
                "suburb": "Temple",
                "country": "United Kingdom",
                "postcode": "EC2Y 5HN",
                "country_code": "gb",
                "house_number": "150",
                "state_district": "Greater London"
            },
            "rate": "3",
            "wikidata": "Q60308",
            "kinds": "fortifications,historic,interesting_places,other_fortifications",
            "voyage": "https://en.wikivoyage.org/wiki/Walk%20the%20London%20Wall",
            "sources": {
                "geometry": "wikidata",
                "attributes": [
                    "wikidata"
                ]
            },
            "otm": "https://opentripmap.com/en/card/Q60308",
            "wikipedia": "https://en.wikipedia.org/wiki/London%20Wall",
            "image": "https://commons.wikimedia.org/wiki/File:London_Roman_Wall_-_surviving_section_by_Tower_Hill_gardens.jpg",
            "preview": {
                "source": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/London_Roman_Wall_-_surviving_section_by_Tower_Hill_gardens.jpg/400px-London_Roman_Wall_-_surviving_section_by_Tower_Hill_gardens.jpg",
                "height": 300,
                "width": 400
            },
            "wikipedia_extracts": {
                "title": "en:London Wall",
                "text": "The London Wall was a defensive wall first built by the Romans around the strategically important port town of Londinium in c. AD 200. It has origins as an initial mound wall and ditch from c. AD 100 and an initial fort, now called Cripplegate fort after the city gate that was positioned within its northern wall later on, built in 120-150 where it was then expanded upon by Roman builders into a city-wide defence. Over time, as Roman influence waned through the departure of the Roman army in c. 410, their withdrawal led to its disrepair, as political power on the island dispersed through the Heptarchy (seven kingdoms) period of Anglo-Saxon England. From the conquest of William the Conqueror, successive medieval restorations and repairs to its use have been undertaken. This wall largely defined the boundaries of the City of London until the later Middle Ages, when population rises and the development of towns around the city blurred the perimeter.",
                "html": "<p>The <b>London Wall</b> was a defensive wall first built by the Romans around the strategically important port town of Londinium in <abbr title=\"circa\">c.</abbr> AD 200. It has origins as an initial mound wall and ditch from <abbr title=\"circa\">c.</abbr> AD 100 and an initial fort, now called Cripplegate fort after the city gate that was positioned within its northern wall later on, built in 120-150 where it was then expanded upon by Roman builders into a city-wide defence. Over time, as Roman influence waned through the departure of the Roman army in <abbr title=\"circa\">c.</abbr> 410, their withdrawal led to its disrepair, as political power on the island dispersed through the Heptarchy (seven kingdoms) period of Anglo-Saxon England. From the conquest of William the Conqueror, successive medieval restorations and repairs to its use have been undertaken. This wall largely defined the boundaries of the City of London until the later Middle Ages, when population rises and the development of towns around the city blurred the perimeter.</p>"
            },
            "point": {
                "lon": -0.09694443643093109,
                "lat": 51.51750183105469
            }
        }
        self.assertEqual(self.expected, OpenTripMapApi.get_activity_details(self.pass_api_key, "Q60308"))


def coordinates_suite():
    coord_suite = unittest.TestSuite()
    coord_suite.addTest(TestGetCoordinatesFunction('test_coordinates_valid_London'))
    coord_suite.addTest(TestGetCoordinatesFunction('test_coordinates_valid_Tokyo'))
    coord_suite.addTest(TestGetCoordinatesFunction('test_coordinates_invalid_minus_51_point_223_and_100_point_100'))
    coord_suite.addTest(TestGetCoordinatesFunction('test_coordinates_invalid_sefwr4356yth'))


    coord_suite.addTest(TestGetCoordinatesFunction('test_coordinates_invalid_empty'))
    coord_suite.addTest(TestGetCoordinatesFunction('test_coordinates_boundary_long_city_name'))
    coord_suite.addTest(TestGetCoordinatesFunction('test_coordinates_boundary_shortest_city_name'))
    return coord_suite


def activities_suite():
    act_suite = unittest.TestSuite()
    act_suite.addTest(
        TestGetActivitiesFunction('test_activities_valid_London_51_point_50853_minus_0_point_12574_churches'))
    act_suite.addTest(TestGetActivitiesFunction('test_activities_invalid_city_name_Lo'))
    act_suite.addTest(TestGetActivitiesFunction('test_activities_invalid_lat_1000'))
    act_suite.addTest(TestGetActivitiesFunction('test_activities_invalid_lon_1000'))
    act_suite.addTest(TestGetActivitiesFunction('test_activities_invalid_kinds_none'))
    return act_suite


def activities_details_suite():
    act_details_suite = unittest.TestSuite()
    act_details_suite.addTest(TestGetActivityDetailsFunction('test_xid_valid_Q17663855'))
    act_details_suite.addTest(TestGetActivityDetailsFunction('test_xid_invalid_17663855Q'))
    act_details_suite.addTest(TestGetActivityDetailsFunction('test_xid_boundary_small_Q60308'))
    return act_details_suite


if __name__ == "__main__":
    unittest.main(verbosity=1)
    # runner = unittest.TextTestRunner()
    # runner.run(coordinates_suite())
    # runner.run(activities_suite())
    # runner.run(activities_details_suite())

    # the above can be uncommented to run the suite of tests from terminal or commandline