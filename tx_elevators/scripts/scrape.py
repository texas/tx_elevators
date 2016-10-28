"""
Process input csv file.

You may see the same data change every time you run this script. That is because
there are dirty entries with duplicate primary keys.

"""
import csv
import logging
import sys

from obj_update import obj_update_or_create
from tx_elevators.models import Building, Elevator
from tqdm import tqdm


logger = logging.getLogger('tx_elevators.scrape')


def format_row(row):
    # trim white space
    for key, value in row.items():
        row[key] = value.strip()
    # trim time off, set null
    date_fields = ['DT_CRT_INS', 'DT_EXPIRY', 'ELV_5YEAR']
    for key in date_fields:
        value = row[key].split(' ', 1)[0]
        if value == '1900-01-01':
            value = None
        row[key] = value or None
    return row


def process_row(row):
    default_data = dict(
        name_1=row['BNAME1'],
        name_2=row['BNAME2'],
        address_1=row['BADDR1'],
        address_2=row['BADDR2'],
        city=row['BCITY'],
        zip_code=row['BZIP'],
        county=row['BCOUNTY'],
        owner=row['ONAME1'],
        contact=row['CNAME1'],
    )
    building, __ = obj_update_or_create(
        Building, elbi=row['LICNO'], defaults=default_data)

    default_data = dict(
        tdlr_id=row['IDNO'],
        last_inspection=row['DT_CRT_INS'],
        next_inspection=row['DT_EXPIRY'],
        last_5year=row['ELV_5YEAR'],
        equipment_type=row['EQUIPMENT_TYPE'],
        drive_type=row['DRIVE_TYPE'],
        floors=row['FLOORS'],
        year_installed=row['YR_INSTALL'],
        building=building
    )
    elevator, __ = obj_update_or_create(
        Elevator, decal=row['SUB_NO'], defaults=default_data)


def process(path):
    with open(path, 'rU') as f:
        reader = csv.DictReader(f)
        for total, row in enumerate(f):  # subtract 1 for header row
            pass
        f.seek(0)
        for row in tqdm(reader, total=total, leave=True):
            try:
                process_row(format_row(row))
            except Exception as e:
                logger.error(e)
                import ipdb
                ipdb.set_trace()
                raise
        print('')  # Fix for tqdm leave=True does not print a newline


def post_process():
    """Manually clean known bad data."""
    # guesses
    Elevator.objects.filter(decal=60678, floors=200).update(floors=10)
    # Elevator.objects.filter(year_installed__gt=2013).update(year_installed=None)

if __name__ == "__main__":
    import django; django.setup()  # NOQA
    path = sys.argv[1]
    process(path)
    post_process()
