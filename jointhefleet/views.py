from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from django.core.paginator import Paginator
from jointhefleet.models import Operation, Member, Killmail
import md5, datetime, json, urllib2
from jointhefleet.forms import create_operation_form, edit_operation_form, add_killmail_form
from django.db.models import Count

def is_fc(user):
    return user.groups.filter(name='Alliance FC').exists()

def is_movs(user):
    return user.groups.filter(name='Movingstar').exists()

def check_trusted(func):
    def check(request, *args, **kwargs):
        trusted = request.META.get('HTTP_EVE_TRUSTED')

        if trusted == "Yes":
            return func(request, *args, **kwargs)
        else:
            return render(request, 'jointhefleet/err_not_trusted.html')

        ret = func(request, *args, **kwargs)
    return check

def index(request):
    '''
    top_character = Member.objects.values('member_id', 'member_name').annotate(id_count=Count('member_id')).order_by('-id_count')[:10]
    top_fc = Operation.objects.values('fc_id', 'fc_name').annotate(id_count=Count('fc_id')).order_by('-id_count')[:10]
    top_corp = Member.objects.values('member_corp_id', 'member_corp_name').annotate(id_count=Count('member_corp_id')).order_by('-id_count')[:10]
    '''

    return render(request, 'jointhefleet/index.html')

def view_history(request):
    if is_fc(request.user) == False and is_movs(request.user) == False:
        return render(request, 'jointhefleet/err_not_allowed.html')

    pages = Paginator(Operation.objects.all().order_by('-date_opd'), 25)
    Operations = pages.page(1)

    top_character = Member.objects.values('member_id', 'member_name').annotate(id_count=Count('member_id')).order_by('-id_count')[:10]
    top_fc = Operation.objects.values('fc_id', 'fc_name').annotate(id_count=Count('fc_id')).order_by('-id_count')[:10]
    top_corp = Member.objects.values('member_corp_id', 'member_corp_name').annotate(id_count=Count('member_corp_id')).order_by('-id_count')[:10]

    return render(request, 'jointhefleet/fleet_history.html', {'Operations':Operations, 'top_character': top_character, 'top_fc': top_fc, 'top_corp': top_corp})

@check_trusted
def join_operation(request, security_code):
    is_Operation_exist = Operation.objects.filter(security_code=security_code).count()
    if is_Operation_exist != 1:
        return render(request, 'jointhefleet/err_not_found.html')

    Operation_ = Operation.objects.get(security_code=security_code)
    info_ = {
        'name' : request.META.get('HTTP_EVE_CHARNAME'),
        'charid' : request.META.get('HTTP_EVE_CHARID'),
        'corp' : request.META.get('HTTP_EVE_CORPNAME'),
        'corpid' : request.META.get('HTTP_EVE_CORPID'),
        'alliance' : request.META.get('HTTP_EVE_ALLIANCENAME'),
        'allianceid' : request.META.get('HTTP_EVE_ALLIANCEID'),
        'ship' : request.META.get('HTTP_EVE_SHIPTYPENAME'),
        'shipid' : request.META.get('HTTP_EVE_SHIPTYPEID'),
        'system' : request.META.get('HTTP_EVE_SOLARSYSTEMNAME'),
        'join_time' : datetime.datetime.now().time().strftime('%H:%M:%S'),
    }

    if Operation_.is_opened() != True:
        return render(request, 'jointhefleet/err_not_opened.html')

    is_exist_member_ = Member.objects.filter(operation=Operation_.id, member_id=info_['charid']).count()
    if is_exist_member_ != 0:
        return render(request, 'jointhefleet/err_already_joined.html')

    Member_ = Member()
    Member_.operation = Operation_
    Member_.member_id = info_['charid']
    Member_.member_name = info_['name']
    Member_.member_ship_id = info_['shipid']
    Member_.member_ship_name = info_['ship']
    Member_.member_system = info_['system']
    Member_.member_corp_id = info_['corpid']
    Member_.member_corp_name = info_['corp']
    Member_.join_time = info_['join_time']
    Member_.save()

    return render(request, 'jointhefleet/join.html', {'Operation':Operation_, 'Info': info_, })

def create_operation(request):
    if is_fc(request.user) == False and is_movs(request.user) == False:
        return render(request, 'jointhefleet/err_not_allowed.html')

    data = {
        'fc_id' : request.META.get('HTTP_EVE_CHARID'),
        'fc_name' : request.META.get('HTTP_EVE_CHARNAME'),
        'date_opd' : datetime.datetime.now(),
    }

    if request.method == 'POST':
        form = create_operation_form(request.POST)
        if form.is_valid():
            operation_ = Operation()
            operation_.code = request.POST.get('code','')
            operation_.date_opd = request.POST.get('date_opd','')
            operation_.category = request.POST.get('category','')
            operation_.fc_id = request.POST.get('fc_id','')
            operation_.fc_name = request.POST.get('fc_name','')
            operation_.security_code = md5.new(operation_.code.encode('ascii', 'ignore') + operation_.date_opd + operation_.fc_id).hexdigest()
            operation_.save()
            return redirect('/jointhefleet/' + str(operation_.id))
    else:
        form = create_operation_form(initial=data)

    return render(request, 'jointhefleet/create.html', {'form': form, })

def view_operation(request, operation_id):
    if is_fc(request.user) == False and is_movs(request.user) == False:
        return render(request, 'jointhefleet/err_not_allowed.html')

    Operation_ = Operation.objects.get(id=operation_id)
    Member_ = Member.objects.filter(operation=operation_id)
    Killmail_ = Killmail.objects.filter(operation=operation_id).order_by('-totalValue')
    '''
    Opdetail_ = {
        '' : ,
    }
    '''
    return render(request, 'jointhefleet/view.html', {'Operation': Operation_, 'Member': Member_, 'numofMembers': Member_.count(), 'Killboard':Killmail_ })

def edit_operation(request, operation_id):
    if is_fc(request.user) == False and is_movs(request.user) == False:
        return render(request, 'jointhefleet/err_not_allowed.html')

    Operation_ = Operation.objects.get(id=operation_id)

    data = {
        'code' : Operation_.code,
        'fc_id' : Operation_.fc_id,
        'fc_name' : Operation_.fc_name,
        'date_opd' : Operation_.date_opd,
        'date_fin' : Operation_.date_fin,
        'category' : Operation_.category,
        'state' : Operation_.state,
        'acquired' : Operation_.acquired,
        'remarks' : Operation_.remarks,
        'killboard' : Operation_.killboard,
        'profit' : Operation_.profit,
    }

    if request.method == 'POST':
        form = edit_operation_form(request.POST)
        if form.is_valid():
            Operation_.code = request.POST.get('code','')
            Operation_.date_opd = request.POST.get('date_opd','')
            if request.POST.get('date_fin','') != '' :
                Operation_.date_fin = request.POST.get('date_fin','')
            Operation_.category = request.POST.get('category','')
            Operation_.fc_id = request.POST.get('fc_id','')
            Operation_.fc_name = request.POST.get('fc_name','')
            Operation_.state = request.POST.get('state','')
            Operation_.acquired = request.POST.get('acquired','')
            Operation_.remarks = request.POST.get('remarks','')
            Operation_.killboard = request.POST.get('killboard','')
            Operation_.profit = request.POST.get('profit','')
            Operation_.save()
            return redirect('/jointhefleet/' + str(Operation_.id))
    else:
        form = edit_operation_form(initial=data)

    return render(request, 'jointhefleet/edit.html', {'form': form, 'Operation':Operation_,})

def add_killmail(request, operation_id):
    if is_fc(request.user) == False and is_movs(request.user) == False:
        return render(request, 'jointhefleet/err_not_allowed.html')

    Operation_ = Operation.objects.get(id=operation_id)

    if request.method == 'POST':
        form = add_killmail_form(request.POST)

        # Fetch Killmail form zKillboard
        if 'fetch' in request.POST:
            killData = urllib2.urlopen('http://zkillboard.com/api/killID/' + request.POST.get('killID','').encode('ascii', 'ignore'))
            data = json.load(killData)

            if data[0]:
                killInfo = {
                    'killID' : data[0].get('killID'),
                    'solarSystemID': data[0].get('solarSystemID'),
                    'killTime' : data[0].get('killTime').encode('ascii', 'ignore'),
                    'shipTypeID': data[0].get('victim').get('shipTypeID'),
                    'characterID': data[0].get('victim').get('characterID'),
                    'characterName': data[0].get('victim').get('characterName').encode('ascii', 'ignore'),
                    'corporationID': data[0].get('victim').get('corporationID'),
                    'corporationName': data[0].get('victim').get('corporationName').encode('ascii', 'ignore'),
                    'allianceID': data[0].get('victim').get('allianceID'),
                    'allianceName': data[0].get('victim').get('allianceName').encode('ascii', 'ignore'),
                    'totalValue': data[0].get('zkb').get('totalValue'),
                }
                form = add_killmail_form(initial=killInfo)
            return render(request, 'jointhefleet/addkillmail.html', {'form':form, 'Operation':Operation_,})

        if 'add' in request.POST:
            if form.is_valid():
                killboard = Killmail()
                killboard.operation_id = Operation_.id
                killboard.killID = request.POST.get('killID','')
                killboard.solarSystemID = request.POST.get('solarSystemID','')
                killboard.killTime = request.POST.get('killTime','')
                killboard.shipTypeID = request.POST.get('shipTypeID','')
                killboard.characterID = request.POST.get('characterID','')
                killboard.characterName = request.POST.get('characterName','')
                killboard.corporationID = request.POST.get('corporationID','')
                killboard.corporationName = request.POST.get('corporationName','')
                killboard.allianceID = request.POST.get('allianceID','')
                killboard.allianceName = request.POST.get('allianceName','')
                killboard.totalValue = request.POST.get('totalValue','')
                killboard.save()
                return redirect('/jointhefleet/' + str(Operation_.id))

    else:
        form = add_killmail_form()

    return render(request, 'jointhefleet/addkillmail.html', {'form':form, 'Operation':Operation_,})

def not_found(request, operation_id):
    return render(request, 'jointhefleet/err_not_found.html')
