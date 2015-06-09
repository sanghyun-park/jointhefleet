from django import forms
from django.forms.models import ModelForm
from datetime import datetime
from jointhefleet.models import Operation, Member, Killmail

'''
class create_operation_form(forms.Form):
    code = forms.CharField(label='Code Name', max_length=100)
    date_opd = forms.DateTimeField(label='Start Time',
                    initial = datetime.now)

    OP_CATEGORY = (
        ('Alliance Operation', (
                ('ROM', 'Roaming'),
                ('CTA', 'CTA'),
                ('TRN', 'Training'),
                ('ETC', 'Etc.'),
            ),
        ),
        ('Movingstar Operation', (
                ('WRR', 'Mission WRR'),
                ('MWF', 'Movingstar Wormhole Fleet'),
            ),
        ),
    )
    category = forms.ChoiceField(label='Category', choices=OP_CATEGORY)

    fc_id = forms.IntegerField(label='FC ID')
    fc_name = forms.CharField(label='FC Name', max_length=50)
'''

class create_operation_form(ModelForm):
    class Meta:
        model = Operation
        fields = ['code', 'date_opd', 'category', 'fc_id', 'fc_name']

class edit_operation_form(ModelForm):
    class Meta:
        model = Operation
        fields = ['code', 'date_opd', 'date_fin', 'category', 'state', 'fc_id', 'fc_name', 'acquired', 'remarks', 'profit']

class add_killmail_form(ModelForm):
    class Meta:
        model = Killmail
        fields = ['killID', 'solarSystemID', 'killTime', 'shipTypeID', 'characterID', 'characterName', 'corporationID', 'corporationName', 'allianceID', 'allianceName', 'totalValue']
