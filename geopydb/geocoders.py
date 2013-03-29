import anydbm
import json

from geopy import geocoders


class GoogleV3(object):
    geocoder = None

    def __init__(self, *args, **kwargs):
        self.geocoder = geocoders.GoogleV3(*args, **kwargs)

    def geocode(self, address):
        store = anydbm.open('GoogleV3_cache', 'c')
        key = address
        value = store.get(key, None)
        if value is None:
            try:
                value_raw = self.geocoder.geocode(address)
                value = json.dumps(value_raw)
                store[key] = value
                print "value retrieved from service"
                return value_raw
            except (ValueError, geocoders.base.GeocoderResultError) as e:
                value = str(e)
                store[key] = value
                raise e
        store.close()
        print "value retrieved from db"
        try:
            value_raw = json.loads(value)
        except ValueError:
            raise ValueError(value)
        return value_raw
