import csv
import logging
import sys

from tx_elevators.models import Building, Elevator


def format_row(row):
    # trim time off
    date_fields = ['DT_CRT_INS', 'DT_EXPIRY', 'ELV_5YEAR']
    for key in date_fields:
        row[key] = row[key].split(' ', 1)[0]
    # trim white space
    for key, value in row.items():
        row[key] = value.strip()
    return row


def process_row(row):
    default_data = dict(
        name_1=row['BNAME1'],
        name_2=row['BNAME2'],
    )
    building, created = Building.objects.get_or_create(
        elbi=row['LICNO'],
        defaults=default_data,
    )

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


def process(path):
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            process_row(format_row(row))


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    path = sys.argv[1]
    process(path)
