from django.core.urlresolvers import reverse
from django.db import models


class Building(models.Model):
    """Some place with an address that holds `Elevator` object(s)."""
    # LICNO
    elbi = models.IntegerField(
        u'Building Number',
        unique=True,
        help_text='The Building Number is a TDLR issued number.',
    )
    # BNAME1
    name_1 = models.CharField(max_length=100)
    # BNAME2
    name_2 = models.CharField(max_length=100)
    # BADDR1
    address_1 = models.CharField(max_length=100)
    # BADDR2
    address_2 = models.CharField(max_length=100)
    # BCITY
    city = models.CharField(max_length=50)
    # BZIP
    zip_code = models.CharField(max_length=5)
    # BCOUNTY
    # ONAME1
    # CNAME1

    def __unicode__(self):
        return u"{0.name_1} {0.city}".format(self)

    def get_absolute_url(self):
        return reverse('tx_elevators:building_detail',
            kwargs={'elbi': self.elbi})


class Elevator(models.Model):
    """Something humans use to go up a `Building`."""
    # IDNO
    tdlr_id = models.IntegerField(
        u'Texas Department of Licensing and Regulation ID',
    )
    # SUB_NO
    decal = models.IntegerField(
        u'Equipment Identification Number',
        unique=True,
        help_text=('Decal# is a TDLR number issued to a particular elevator or'
                   ' piece of equipment.')
    )
    # DT_CRT_INS
    last_inspection = models.DateField(
        u'Date of Last Certified Inspection',
        null=True,  # sometimes this is empty for some reason
    )
    # DT_EXPIRY
    next_inspection = models.DateField(
        u'Date of Next Inspection',
    )
    # ELV_5YEAR
    last_5year = models.DateField(
        u'Date of Last 5 Year Test',
    )
    # EQUIPMENT_TYPE
    equipment_type = models.CharField(
        u'Equipment Type',
        # TODO choices
        max_length=26,
    )
    # DRIVE_TYPE
    drive_type = models.CharField(
        u'Machine Drive Type',
        # TODO choices
        max_length=20,
    )
    # FLOORS
    floors = models.IntegerField()
    # YR_INSTALL
    year_installed = models.IntegerField()

    building = models.ForeignKey(Building)

    def __unicode__(self):
        return u"{0.building} {0.floors} ({0.year_installed})".format(self)
