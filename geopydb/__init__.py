"""
A simple wrapper around geopy that caches to disk.
"""
__version__ = "0.1.0-dev"


import anydbm
import json

from geopy import geocoders


class GoogleV3(object):
    geocoder = None
    store = None

    def __init__(self, *args, **kwargs):
        self.geocoder = geocoders.GoogleV3(*args, **kwargs)
        self.store = anydbm.open('GoogleV3_cache', 'c')

    def geocode(self, address):
        key = address
        value = self.store.get(key, None)
        if value is None:
            try:
                value_raw = self.geocoder.geocode(address)
                value = json.dumps(value_raw)
                self.store[key] = value
                print "value retrieved from service"
                return value_raw
            except ValueError as e:
                value = str(e)
                self.store[key] = value
                raise e
        print "value retrieved from db"
        try:
            value_raw = json.loads(value)
        except ValueError:
            raise ValueError(value)
        return value_raw


if __name__ == "__main__":
    # this is my test suite lol
    g = GoogleV3()  # instead of from geopy.geocoders import GoogleV3
    place, (lat, lng) = g.geocode("10900 Euclid Ave in Cleveland")
    print "%s: %.5f, %.5f" % (place, lat, lng)
    # 10900 Euclid Avenue, Cleveland, OH 44106, USA: 41.50726, -81.60701
