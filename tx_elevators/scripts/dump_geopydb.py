#!/usr/bin/env python
"""
Dump existing geo data into an existing anydbm database.

You can tell which entreis were manually inserted because they will be missing
"USA" and will be in uppercase. You should make a backup of the original
database before running this script.
"""
import anydbm
import json

from tx_elevators.models import Building


if __name__ == "__main__":
    qs = Building.objects.exclude(latitude=None)
    store = anydbm.open('GoogleV3_cache', 'w')

    new_entries = 0
    old_entries = 0

    for building in qs:
        key = building._geocode_prep_lookup()
        value = store.get(key, None)
        if value is None:
            new_entries += 1
            new_value = json.dumps((key, (building.latitude, building.longitude)))
            store[key] = new_value

        else:
            old_entries += 1
    store.close()
    print "New: %s" % new_entries
    print "Old: %s" % old_entries
