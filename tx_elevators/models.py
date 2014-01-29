from django.core.urlresolvers import reverse
from django.db import models
# from django.utils.text import slugify
from django.template.defaultfilters import slugify


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
            kwargs={'elbi': self.elbi, 'slug': slugify(self.name_1)})

    def get_geo_query(self):
        lookup_bits = []
        if self.address_1:
            lookup_bits.append(self.address_1)
        if self.city:
            lookup_bits.append(self.city)
        if not lookup_bits:
            return
        lookup = ', '.join(map(str, lookup_bits))
        return lookup

    def geocode(self, lookup=None, force=False):
        """
        Geocode this building.

        Latitudes should be between 25 50' and 36 30'
        Longitude should be between -93 31' and -106 39'
        """
        from geopydb import geocoders
        g = geocoders.GoogleV3()
        # XXX the zip code is wrong sometimes
        __, (lat, lng) = g.geocode(self.get_geo_query(), exactly_one=True,
            components=dict(
                postal_code=self.zip_code,
            ),
            force=force,
        )
        self.latitude = lat
        self.longitude = lng
        self.save()

    def neighbors(self, d=0.001):
        """
        Get neighboring buildings.

        Defaults to a very tiny radius.
        """
        return Building.objects.filter(
            latitude__range=(self.latitude - d, self.latitude + d),
            longitude__range=(self.longitude - d, self.longitude + d),
        )

    def ungeocode(self):
        """
        Mark this geocode as wrong.
        """
        for building in self.neighbors():
            building.geocode(force=True)


class ElevatorManager(models.Manager):
    use_for_related_fields = True

    def for_table(self):
        """
        The queryset that should be used inside the building_detail template.
        """
        return self.get_query_set().order_by(
            '-floors',
            '-equipment_type',
            'drive_type',
        )


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

    # managers
    objects = ElevatorManager()

    def __unicode__(self):
        return u"{0.building} {0.floors} ({0.year_installed})".format(self)

    @property
    def css_classes(self):
        return self.equipment_type.split(' ')[0].lower()
