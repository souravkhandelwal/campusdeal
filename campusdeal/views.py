from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from campusdeal.models import User, Item, Bidder, History, StudentAddress, FacultyAddress
from ftplib import FTP
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from datetime import datetime

def index(request):
    return render_to_response('campusdeal/index.html', context_instance = RequestContext(request))

def register(request):
    return render_to_response('campusdeal/register.html', context_instance = RequestContext(request))
    
def reg_submit(request):
    try :
        username = request.POST['iitk_username']
        password = request.POST['iitk_password']
        n = request.POST['full_name']
        sex = request.POST['sex']
        roll = request.POST['rollno']
        isStudent = request.POST['ask']
        if isStudent=='Y':
            student_hall = request.POST['student_hall']
            student_roomno = request.POST['student_roomno']
        else:
            other_type = request.POST['other_type']
            other_roomno = request.POST['other_roomno']
        dept = request.POST['department']
        phone = request.POST['phoneno']
        
        try:
            ftp = FTP('vyom.cc.iitk.ac.in', username, password)
            ftp.quit()
            p=User(name=n,
                roll=roll, 
                email=username+"@iitk.ac.in",
                phone=phone,
                isStudent=isStudent,
                dept=dept,
                sex=sex)
            if len(User.objects.filter(email=username+"@iitk.ac.in"))>0:
                return render_to_response('campusdeal/register.html', {'err':"already_registered"} , context_instance = RequestContext(request))
            else:
                p.save() 
            if isStudent=='Y':
                p.studentaddress_set.create(hall = student_hall, room = student_roomno)
            else:
                p.facultyaddress_set.create(typename = other_type, houseno = other_roomno)
        except:
            return render_to_response('campusdeal/register.html', {'err':"login_error"} , context_instance = RequestContext(request))

        request.session['userid'] = p.id
        items = Item.objects.order_by('-timestamp').all()
        if len(items)>4:
            request.session['last_index'] = 4
            return render_to_response('campusdeal/home.html', {'recent':False, 'items':items[0:4]}, context_instance = RequestContext(request))
        else:
            request.session['last_index'] = len(items)
            return render_to_response('campusdeal/home.html', {'recent':False, 'items':items[0:len(items)]}, context_instance = RequestContext(request))
   
    except:
        return render_to_response('campusdeal/register.html', {'err':"invalid_details"} , context_instance = RequestContext(request))

def logout(request):
    try :
        del request.session['userid']
    except :
        pass
    return render_to_response('campusdeal/index.html',context_instance = RequestContext(request))

def add_item(request):
    return render_to_response('campusdeal/newitem.html', {'error' : False}, context_instance = RequestContext(request))
    
def item_added(request):
    try :
        d = request.POST['item_desc']
        t = request.POST['item_title']
        p = request.POST['min_bid']
        c = request.POST['typeofitem']
        i = request.FILES['itemimage']
        p=Item(sellerID = User.objects.get(pk=1),
            category = c,
            price = p,
            image = i,
            title = t,
            description = d,
            timestamp = datetime.now(),
            soldPrice = 0,
            status = "Added at "+str(datetime.now()).split('.')[0])
        p.save()
        return HttpResponseRedirect('/campusdeal/myitems/static')
    except:
        return render_to_response('/campusdeal/newitem.html', {'error' : True}, context_instance = RequestContext(request))
    
def home(request):
    u = ""
    password = ""
    if not ('userid' in request.session):
        username = request.POST['iitk_username']
        password = request.POST['iitk_password']
        try:
            ftp = FTP('vyom.cc.iitk.ac.in', username, password)
            ftp.quit()
        except:
            return render_to_response('campusdeal/index.html', {'err':"login_error"}, context_instance = RequestContext(request))
			# This is to see the user is registered or not. Redirect to start page.
			# Need to display message
        try:
            User.objects.get(email=username+"@iitk.ac.in")
            # return HttpResponseRedirect("campusdeal/home.html")
        except:
            return render_to_response('campusdeal/register.html', {'err': "not_registered"}, context_instance = RequestContext(request))
    else :
        userid = request.session['userid']
        username = User.objects.get(id=userid).email.split("@")[0]

    u = User.objects.get(email=username+"@iitk.ac.in")
    request.session['userid'] = u.id
    items = Item.objects.order_by('-timestamp').all()
    if len(items)>4:
        request.session['last_index'] = 4
        return render_to_response('campusdeal/home.html', {'recent':False, 'items':items[0:4]}, context_instance = RequestContext(request))
    else:
        request.session['last_index'] = len(items)
        return render_to_response('campusdeal/home.html', {'recent':False, 'items':items[0:len(items)]}, context_instance = RequestContext(request))

def item(request, item_id):
    item = Item.objects.get(id=item_id)
    userid = request.session['userid']
    u = User.objects.get(id=userid)
    prev_bids=Bidder.objects.filter(bidderID = u, item = item)
    if(len(prev_bids) > 0):
        return render_to_response('campusdeal/item.html', {'item':item, 'prev_bid':True, 'previousBid':prev_bids[0].bid}, context_instance = RequestContext(request))
    else:
        return render_to_response('campusdeal/item.html', {'item':item, 'prev_bid':False, 'previousBid':0}, context_instance = RequestContext(request))

def user_info(request):
    userid = request.GET['q']
    user = User.objects.get(id = userid)
    s = user.name+"****"+user.email+"****"+user.phone+"****"
    if (user.isStudent == 'Y'):
        address = StudentAddress.objects.get(user=user)
        s += address.hall+" "+address.room
    else:
        address = FacultyAddress.objects.get(user = user)
        s+= address.typename+" "+address.houseno
    return HttpResponse(s)

def updateBidder(request, item_id):
    current_bid = request.GET['p']
    item_id = request.GET['q']
    item = Item.objects.get(id=item_id)
    userid = request.session['userid']
    user = User.objects.get(id=userid)
    other_bids = Bidder.objects.filter(bidderID = user, item = item)
    if len(other_bids)==1:
        other_bid = other_bids[0]
        if (float(current_bid) > float(other_bid.bid)):
            other_bid.bid = current_bid
            other_bid.save()
            item.timestamp = datetime.now()
            item.status = "Last bid at " + str(datetime.now()).split('.')[0] + 'by ' + user.name
            item.save()
            return HttpResponse("Successful Bid : Rs. " + str(current_bid))
        else:
            return HttpResponse("current bid should more than previous bid %s" % other_bid.bid)
    else:
        if (float(current_bid) >= float(item.price)):
            p=Bidder(bidderID=user, item=item, bid=current_bid)
            p.save()
            item.timestamp = datetime.now()
            item.status = "Last bid at " + str(datetime.now()).split('.')[0] + 'by ' + user.name
            item.save()
            return HttpResponse("Successful Bid : Rs. " + str(current_bid))
        else:
            return HttpResponse("bid must be more than base price")

def next_recent(request):
    if 'userid' in request.session:
		if 'last_index' in request.session:
			pos = request.session['last_index']
			items = Item.objects.order_by('-timestamp').all()
			if pos+4<len(items):
				request.session['last_index'] = pos+4
				return render_to_response('campusdeal/home.html', {'recent':False, 'items':items[pos:pos+4]}, context_instance = RequestContext(request))
			else:
				request.session['last_index'] = len(items)
				return render_to_response('campusdeal/home.html', {'recent':False, 'items':items[pos:len(items)]}, context_instance = RequestContext(request))


def previous_recent(request):
    if 'userid' in request.session:
        if 'last_index' in request.session:
			pos = request.session['last_index']
			items = Item.objects.order_by('-timestamp').all()
			if pos-4>=0:
				request.session['last_index'] = pos
				return render_to_response('campusdeal/home.html', {'recent':False, 'items':items[pos-4:pos]}, context_instance = RequestContext(request))
			else:
				if len(items)>4:
					request.session['last_index'] = 4
					return render_to_response('campusdeal/home.html', {'recent':False, 'items':items[0:4]}, context_instance = RequestContext(request))
				else:
					request.session['last_index'] = len(items)
					return render_to_response('campusdeal/home.html', {'recent':False, 'items':items[0:len(items)]}, context_instance = RequestContext(request))

def myitems(request):
    userid = request.session['userid']
    myitemlist = Item.objects.filter(sellerID = User.objects.get(id=userid)).order_by('-id')
    s = str(len(myitemlist))+""
    for myitem in myitemlist:
        s += "****"
        s += str(myitem.image.name)
        s += "****"
        s += str(myitem.title)
        s += "****"
        s += str(myitem.price)
        s += "****"
        s += str(myitem.category)
        s += "****"
        s += str(myitem.id)
    return HttpResponse(s)
    
def myitems_static(request) :
    return render_to_response('campusdeal/myitems.html', {}, context_instance = RequestContext(request))

def bids(request):
    itemid = request.GET['q']
    item = Item.objects.get(id = itemid)
    bidlist = Bidder.objects.filter(item=item)
    s = str(len(bidlist))+""
    for bid in bidlist:
        s += "****"
        s += str(bid.id)
        s += "****"
        s += str(bid.bidderID.email)
        s += "****"
        s += str(bid.bidderID.name)
        s += "****"
        s += str(bid.bid)
    return HttpResponse(s)

def accept_bid(request):
    bid_id = request.GET['q']
    
    bid = Bidder.objects.get(id=bid_id)
    
    item = bid.item
    
    item.soldPrice = bid.bid
    
    item.timestamp = datetime.now()
    
    item.status = "Sold at " + str(datetime.now()).split('.')[0] + " to " + bid.bidderID.name +" for " + str(bid.bid)
    
    item.save()
    
    h=History(buyerID=bid.bidderID, itemID = item, price = bid.bid)
    h.save()
    bid.delete()
    return HttpResponse("Transaction Successful")

def mybids(request):
    userid = request.session['userid']
    user = User.objects.get(id=userid)
    bids = Bidder.objects.filter(bidderID = user).order_by('-id')
    return render_to_response('campusdeal/mybids.html', {'bids':bids}, context_instance = RequestContext(request))
    
def remove_bid(request, bid_id):
    bid = Bidder.objects.get(id = bid_id)
    bid.delete()
    return mybids(request)

def all(request):
    items = Item.objects.order_by('-timestamp')
    if len(items)>4:
        request.session['last_index'] = 4
        return render_to_response('campusdeal/home.html', {'recent':False, 'items':items[0:4]}, context_instance = RequestContext(request))
    else:
        request.session['last_index'] = len(items)
        return render_to_response('campusdeal/home.html', {'recent':False, 'items':items[0:len(items)]}, context_instance = RequestContext(request))

def cycles(request):
    items = Item.objects.order_by('-timestamp').filter(category='cycles')
    if len(items)>4:
        request.session['last_index'] = 4
        return render_to_response('campusdeal/home.html', {'recent':False, 'items':items[0:4]}, context_instance = RequestContext(request))
    else:
        request.session['last_index'] = len(items)
        return render_to_response('campusdeal/home.html', {'recent':False, 'items':items[0:len(items)]}, context_instance = RequestContext(request))
 
def electronics(request):
    items = Item.objects.order_by('-timestamp').filter(category='electronics')
    if len(items)>4:
        request.session['last_index'] = 4
        return render_to_response('campusdeal/home.html', {'recent':False, 'items':items[0:4]}, context_instance = RequestContext(request))
    else:
        request.session['last_index'] = len(items)
        return render_to_response('campusdeal/home.html', {'recent':False, 'items':items[0:len(items)]}, context_instance = RequestContext(request))
 
def coolers(request):
    items = Item.objects.order_by('-timestamp').filter(category='coolers')
    if len(items)>4:
        request.session['last_index'] = 4
        return render_to_response('campusdeal/home.html', {'recent':False, 'items':items[0:4]}, context_instance = RequestContext(request))
    else:
        request.session['last_index'] = len(items)
        return render_to_response('campusdeal/home.html', {'recent':False, 'items':items[0:len(items)]}, context_instance = RequestContext(request))
 
def books(request):
    items = Item.objects.order_by('-timestamp').filter(category='books')
    if len(items)>4:
        request.session['last_index'] = 4
        return render_to_response('campusdeal/home.html', {'recent':False, 'items':items[0:4]}, context_instance = RequestContext(request))
    else:
        request.session['last_index'] = len(items)
        return render_to_response('campusdeal/home.html', {'recent':False, 'items':items[0:len(items)]}, context_instance = RequestContext(request))
 
def tickets(request):
    items = Item.objects.order_by('-timestamp').filter(category='tickets')
    if len(items)>4:
        request.session['last_index'] = 4
        return render_to_response('campusdeal/home.html', {'recent':False, 'items':items[0:4]}, context_instance = RequestContext(request))
    else:
        request.session['last_index'] = len(items)
        return render_to_response('campusdeal/home.html', {'recent':False, 'items':items[0:len(items)]}, context_instance = RequestContext(request))

def others(request):
    items = Item.objects.order_by('-timestamp').filter(category='others')
    if len(items)>4:
        request.session['last_index'] = 4
        return render_to_response('campusdeal/home.html', {'recent':False, 'items':items[0:4]}, context_instance = RequestContext(request))
    else:
        request.session['last_index'] = len(items)
        return render_to_response('campusdeal/home.html', {'recent':False, 'items':items[0:len(items)]}, context_instance = RequestContext(request))


def search(request):
    searchString = request.POST['search']
    if searchString == '':
        return render_to_response('campusdeal/home.html', {'recent':False, 'items':[]}, context_instance = RequestContext(request))
    else:
        itemList = Item.objects.filter(title__contains=searchString)
        return render_to_response('campusdeal/home.html', {'recent':True, 'items':itemList}, context_instance = RequestContext(request))