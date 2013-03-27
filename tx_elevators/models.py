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
    county = models.CharField(max_length=20)
    # ONAME1
    owner = models.CharField(max_length=100)
    # CNAME1
    contact = models.CharField(max_length=100)

    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    def __unicode__(self):
        return u"{0.name_1} in {0.city}".format(self)

    def get_absolute_url(self):
        return reverse('tx_elevators:building_detail',
            kwargs={'elbi': self.elbi})

    def geocode(self):
        lookup_bits = []
        if self.name_1:
            lookup_bits.append(self.address_1)
        if self.address_1:
            lookup_bits.append(self.address_1)
        if self.city:
            lookup_bits.append(self.city)
        if self.zip_code:
            lookup_bits.append(self.zip_code)
        if not lookup_bits:
            return
        import geopydb
        g = geopydb.GoogleV3()
        lookup = ','.join(map(str, lookup_bits))
        __, (lat, lng) = g.geocode(lookup)
        self.latitude = lat
        self.longitude = lng
        self.save()


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
        null=True,
    )
    # DT_EXPIRY
    next_inspection = models.DateField(
        u'Date of Next Inspection',
    )
    # ELV_5YEAR
    last_5year = models.DateField(
        u'Date of Last 5 Year Test',
        null=True,
    )
    # EQUIPMENT_TYPE
    # choices:
    # [u'ESCALATOR',
    #  u'NEW EQUIPMENT',
    #  u'STAIR CLIMBER',
    #  u'ELECTRIC ELEVATOR',
    #  u'LIMITED USE LIMITED ACCESS',
    #  u'FREIGHT',
    #  u'WHEELCHAIR LIFT',
    #  u'UNKNOWN',
    #  u'HYDRAULIC ELEVATOR',
    #  u'OTHER',
    #  u'PASSENGER',
    #  u'MOVING SIDEWALK']
    equipment_type = models.CharField(
        u'Equipment Type',
        # TODO choices
        max_length=26,
    )
    # DRIVE_TYPE
    # choices:
    # [u'ELEVATOR DRIVE TYPE',
    #  u'CHAIN',
    #  u'ELECTRIC',
    #  u'UNKNOWN',
    #  u'ROPED SPROCKET',
    #  u'ROPED HYDRAULIC',
    #  u'SCREW',
    #  u'HYDRAULIC',
    #  u'RACK & PINION',
    #  u'WINDING DRUM']
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
