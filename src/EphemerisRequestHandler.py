# Get Ephemeris of each planet
import re
import requests
from datetime import datetime


class Ephemeris_Request_Handler_Impl:

    planetary_ids = {'Sun': [10, 1.989*10**30], 'Mercury': [199, 3.302*10**23], 'Venus': [299, 4.869*10**24],
                     'Earth': [399, 5.972*10**24], 'Mars': [499, 6.417*10**23], 'Jupiter': [599, 1.898*10**27],
                     'Saturn': [699, 5.683*10**26], 'Uranus': [799, 8.681*10**25], 'Neptune': [899, 1.04*10**26]}

    solar_system_barycenter = r"'500@0'"

    payload = {"format": "json", "COMMAND": "", "OBJ_DATA": "YES", "MAKE_EPHEM": "YES", "EPHEM_TYPE": "VECTORS",
               "CENTER": "", "TLIST": ''}

    url = "https://ssd.jpl.nasa.gov/api/horizons.api"

    date = datetime.now().strftime("%Y-%b-%d %H:%M:%S.%f")

    distance_conversion = 10**3

    @classmethod
    def send_request(cls, celestial_objects):
        cls.payload['CENTER'] = cls.solar_system_barycenter
        cls.payload['COMMAND'] = cls.planetary_ids[celestial_objects][0]
        cls.payload['TLIST'] = r"'%s'" % str(cls.date)
        reponse = requests.get(cls.url, params=cls.payload)
        content = reponse.json()
        if content['signature']['version'] != '1.2':
            raise Exception("Using the wrong API!")
        body = content['result']
        coordinate, velocity = cls.parse_reponse_body(body)
        mass = cls.planetary_ids[celestial_objects][1]
        return coordinate, velocity, mass

    @classmethod
    def parse_reponse_body(cls, body):
        coordinate = []
        velocity = []
        coordinate.append(
            float(re.findall("X =(.*)Y", body).pop())*cls.distance_conversion)
        coordinate.append(
            float(re.findall("Y =(.*)Z", body).pop())*cls.distance_conversion)
        velocity.append(float(re.findall("VX=(.*)VY", body).pop())
                        * cls.distance_conversion)
        velocity.append(float(re.findall("VY=(.*)VZ", body).pop())
                        * cls.distance_conversion)

        return coordinate, velocity

# capture mass
# # Mass(?: x10\^23 \(kg\)|, 10\^24 kg)\s*=\s*[~]?([0-9.]+)

# capture mass conversion
# Mass(?: x(10\^\d{2}) \(kg\)|, (10\^\d{2}) kg)\s*=\s*[~]?([0-9.]+)
