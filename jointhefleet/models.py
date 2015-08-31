from django.db import models
from django.contrib.auth.models import User

class Operation(models.Model):
    # Operation Codename
    code = models.CharField(max_length=100, help_text='Operation Code')

    # Operation Date Information
    date_opd = models.DateTimeField('date operated', help_text='Start Time')
    date_fin = models.DateTimeField('date finished', blank=True, null=True,
                help_text='Finish Time')

    # Operation Join Information
    security_code = models.CharField(max_length=32,
                help_text='OP Security Code for join')

    # Operation General Information
    OP_CATEGORY = (
        ('Alliance Operation', (
                ('ROM', 'Roaming'),
                ('CTA', 'CTA'),
                ('TRN', 'Training'),
                ('ETC', 'Etc.'),
            ),
        ),
    )
    category = models.CharField(max_length=3, choices=OP_CATEGORY,
                default='CTA', help_text='Operation Category')

    OP_STATUS = (
        ('OPENED', 'Opened'),
        ('CLOSED', 'Closed'),
        ('DSITED', 'Distributed'),
    )
    state = models.CharField(max_length=6, choices=OP_STATUS, default='OPENED',
                help_text='State of this Operation')

    fc_id = models.IntegerField(help_text='Charactor ID')
    fc_name = models.CharField(max_length=50, help_text='Charactor Name')

    acquired = models.TextField(blank=True, null=True,
                help_text='Acquired Item lists')
    remarks = models.TextField(blank=True, null=True,
                help_text='Remarks')
    killboard = models.TextField(blank=True, null=True,
                help_text='Killboard Links')

    profit = models.IntegerField(blank=True, null=True, default=0, help_text='Profit')

    # is deleted?
    deleted = models.BooleanField(default=False)

    def is_opened(self):
        if self.state == 'OPENED':
            return True
        else:
            return False

    def __unicode__(self):
        return self.code

class Member(models.Model):
    operation = models.ForeignKey('Operation')

    member_id = models.IntegerField()
    member_name = models.CharField(max_length=50)
    member_ship_id = models.IntegerField()
    member_ship_name = models.CharField(max_length=50)
    member_system = models.CharField(max_length=30)
    member_corp_id = models.IntegerField(default=1)
    member_corp_name = models.CharField(default='Not Recorded', max_length=50)

    join_time = models.TimeField('Join Time', help_text="Join Time")
    exit_time = models.TimeField('Exit Time', blank=True, null=True,
                    help_text="Exit Time")

    def __str__(self):
        return self.member_name

class Killmail(models.Model):
    operation = models.ForeignKey('Operation')

    # zKillboard
    killID = models.IntegerField()
    solarSystemID = models.IntegerField()
    killTime = models.DateTimeField()

    # victim
    shipTypeID = models.IntegerField()
    characterID = models.IntegerField()
    characterName = models.CharField(max_length=50)
    corporationID = models.IntegerField()
    corporationName = models.CharField(max_length=50)
    allianceID = models.IntegerField(blank=True, null=True)
    allianceName = models.CharField(blank=True, null=True, max_length=50)

    # value
    totalValue = models.FloatField(blank=True, null=True)
