from django.contrib import admin
from jointhefleet.models import Operation, Member, Killmail

class OperationAdmin(admin.ModelAdmin):
    list_display = ('code', 'date_opd', 'category', 'state', 'fc_name')

class MemberAdmin(admin.ModelAdmin):
    list_display = ('operation', 'member_name', 'member_ship_name', 'member_corp_name')

class KillmailAdmin(admin.ModelAdmin):
    list_display = ('operation', 'killTime', 'shipTypeID', 'characterName', 'corporationName', 'allianceName', 'totalValue')

admin.site.register(Operation, OperationAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Killmail, KillmailAdmin)
