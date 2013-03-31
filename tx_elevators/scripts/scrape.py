"""
Process input csv file.

You may see the same data change every time you run this script. That is because
there are dirty entries with duplicate primary keys.

"""
import csv
import logging
import sys

from tx_elevators.models import Building, Elevator


def setfield(obj, fieldname, value):
    """Fancy setattr with debugging."""
    old = getattr(obj, fieldname)
    if str(old) != str(value):
        setattr(obj, fieldname, value)
        if not hasattr(obj, '_is_dirty'):
            obj._is_dirty = []
        obj._is_dirty.append("%s %s->%s" % (fieldname, old, value))


def update(obj, data):
    """
    Fancy way to update `obj` with `data` dict.

    Returns True if data changed and  was saved.
    """
    for key, value in data.items():
        setfield(obj, key, value)
    if getattr(obj, '_is_dirty', None):
        logger.debug(obj._is_dirty)
        obj.save()
        del obj._is_dirty
        return True


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
    building, created = Building.objects.get_or_create(
        elbi=row['LICNO'],
        defaults=default_data,
    )
    if not created:
        update(building, default_data)

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
    elevator, created = Elevator.objects.get_or_create(
        decal=row['SUB_NO'],
        defaults=default_data,
    )
    if not created:
        update(elevator, default_data)


def process(path):
    with open(path, 'rU') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if not i % 1000:
                logger.info("Processing Row %s" % i)
            try:
                process_row(format_row(row))
            except Exception as e:
                logger.error(e)
                import ipdb
                ipdb.set_trace()
                raise


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    path = sys.argv[1]
    process(path)
