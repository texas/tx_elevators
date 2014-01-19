import anydbm
import json
import logging

from geopy import geocoders


class GoogleV3(object):
    geocoder = None

    def __init__(self, *args, **kwargs):
        self.geocoder = geocoders.GoogleV3(*args, **kwargs)

    def geocode(self, query, force=False, **kwargs):
        """
        Additional args:

            force: force a lookup, bypassing the cache
        """
        logger = logging.getLogger(__name__)
        key = query
        store = anydbm.open('GoogleV3_cache', 'c')
        value = store.get(key, None)
        if force or value is None:
            try:
                value_raw = self.geocoder.geocode(query, **kwargs)
                value = json.dumps(value_raw)
                store[key] = value
                store.close()
                logger.info('value retrieved from service', extra=dict(kwargs,
                    query=query,
                    force=force,
                    key=key,
                    value=key,
                ))
                return value_raw
            except (ValueError, geocoders.base.GeocoderResultError) as e:
                value = str(e)
                store[key] = value
                store.close()
                raise e
        store.close()
        logger.info('value retrieved from db', extra=dict(kwargs,
            query=query,
            force=force,
            key=key,
            value=key,
        ))
        try:
            value_raw = json.loads(value)
        except ValueError:
            raise ValueError(value)
        return value_raw
