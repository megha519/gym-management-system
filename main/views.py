from django.core.mail import EmailMessage
from django.shortcuts import render,redirect
from . import models
from . import forms
import stripe
from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.template.loader import get_template
from django.db.models import Count
from datetime import timedelta
from django.db.models import Count


# home page
def home(request):
    banners = models.Banners.objects.all()
    services= models.Service.objects.all()[:3]
    gimgs = models.GalleryImage.objects.all().order_by('-id')[:9]
    return render(request,'home.html',{'banners':banners,'services':services, 'gimgs':gimgs})

# page
def page_detail(request,id):
    page = models.Page.objects.get(id=id)
    return render(request,'page.html',{'page':page})

# faq
def faq_list(request):
    faq = models.Faq.objects.all()
    return render(request,'faq.html',{'faqs':faq})

# enquiry
def enquiry_list(request):
    msg = ''
    if request.method == 'POST':
        form = forms.EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            msg = 'form has been saved'
    form = forms.EnquiryForm()
    return render(request,'enquiry.html',{'form':form,'msg':msg})

def gallery(request):
    galleries= models.Gallery.objects.all().order_by("-id")
    return render(request,'gallery.html',{'galleries':galleries})

# show gallery photos
def gallery_detail(request,id):
    gallery = models.Gallery.objects.get(id=id)
    gallery_imgs = models.GalleryImage.objects.filter(gallery=gallery).order_by('-id')
    return render(request,'gallery_img.html',{'gallery_imgs':gallery_imgs,'gallery':gallery}) 

def pricing(request):
	pricing=models.SubPlan.objects.annotate(total_members=Count('subscription__id')).all().order_by('price')
	dfeatures=models.SubPlanFeature.objects.all();
	return render(request, 'pricing.html',{'plans':pricing,'dfeatures':dfeatures})

stripe.api_key = 'sk_test_51PZGCFSAtQcMv72ppDGtQzIJyzCGUEHA6SVJj85STDziNjyTetE3odxHUezuFUJsF3Ae0q1s1QpbtcpJNIc3CbdD00BIy5c3Tn'
# Checkout
def checkout(request,plan_id):
	planDetail=models.SubPlan.objects.get(pk=plan_id)
	return render(request, 'checkout.html',{'plan':planDetail})



# signup

def signup(request):
	msg=None
	if request.method=='POST':
		form=forms.SignUp(request.POST)
		if form.is_valid():
			form.save()
			msg='Thank you for register.'
	form=forms.SignUp
	return render(request, 'registration/signup.html',{'form':form,'msg':msg})







def checkout_session(request, plan_id):
    if request.method == 'POST':
        plan = models.SubPlan.objects.get(pk=plan_id)
        customer_name = request.POST['customer_name']
        customer_email = request.POST['customer_email']
        customer_address = request.POST['customer_address']
        customer_city = request.POST['customer_city']
        customer_postal_code = request.POST['customer_postal_code']
        discounted_price = request.POST['discounted_price']  # Get discounted price

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': plan.title,
                    },
                    'unit_amount': int(float(discounted_price) * 100),  # Use discounted price
                },
                'quantity': 1,
            }],
            mode='payment',
            customer_email=customer_email,
            billing_address_collection='required',
            success_url='http://127.0.0.1:8000/pay_success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://127.0.0.1:8000/pay_cancel',
            client_reference_id=plan_id,
            shipping_address_collection={
                'allowed_countries': ['IN'],
            },
            metadata={
                'customer_name': customer_name,
                'customer_address': customer_address,
                'customer_city': customer_city,
                'customer_postal_code': customer_postal_code,
            },
        )
        return JsonResponse({'url': session.url})


def pay_success(request):

    session = stripe.checkout.Session.retrieve(request.GET['session_id'])
    plan_id=session.client_reference_id
    plan=models.SubPlan.objects.get(pk=plan_id)
    user=request.user
    models.Subscription.objects.create(
		plan=plan,
		user=user,
		price=plan.price,
	)
    subject='Order Email'
    html_content=get_template('orderemail.html').render({'title':plan.title})
    from_email='meghana.vishali519@gmail.com'
    msg = EmailMessage(subject, html_content, from_email, ['meghanatankala2004@gmail.com'])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()
    return render(request, 'success.html')

def pay_cancel(request):
    return render(request, 'cancel.html')


# User Dashboard Section Start
def user_dashboard(request):
	current_plan=models.Subscription.objects.get(user=request.user)
	my_trainer=models.AssignSubscriber.objects.get(user=request.user)
	enddate=current_plan.reg_date+timedelta(days=current_plan.plan.validity_days)

	# Notification
	data=models.Notify.objects.all().order_by('-id')
	notifStatus=False
	jsonData=[]
	totalUnread=0
	for d in data:
		try:
			notifStatusData=models.NotifUserStatus.objects.get(user=request.user,notif=d)
			if notifStatusData:
				notifStatus=True
		except models.NotifUserStatus.DoesNotExist:
			notifStatus=False
		if not notifStatus:
			totalUnread=totalUnread+1

	return render(request, 'user/dashboard.html',{
		'current_plan':current_plan,
		'my_trainer':my_trainer,
		'total_unread':totalUnread,
		'enddate':enddate
	})


def update_profile(request):
	msg=None
	if request.method=='POST':
		form=forms.ProfileForm(request.POST,instance=request.user)
		if form.is_valid():
			form.save()
			msg='Data has been saved'
	form=forms.ProfileForm(instance=request.user)
	return render(request, 'user/updateprofile.html',{'form':form,'msg':msg})

def trainerlogin(request):
	msg=''
	if request.method=='POST':
		username=request.POST['username']
		pwd=request.POST['pwd']
		trainer=models.Trainer.objects.filter(username=username,pwd=pwd).count()
		if trainer > 0:
			trainer=models.Trainer.objects.filter(username=username,pwd=pwd).first()
			request.session['trainerLogin']=True
			request.session['trainerid']=trainer.id
			return redirect('/trainerdashboard')
		else:
			msg='Invalid!!'
	form=forms.TrainerLoginForm
	return render(request, 'trainer/login.html',{'form':form,'msg':msg})

def trainerlogout(request):
    if 'trainerLogin' in request.session:
        del request.session['trainerLogin']
    return redirect('/trainerlogin')

def trainerdashboard(request):
	return render(request, 'trainer/dashboard.html')

# Trainer Profile
def trainer_profile(request):
	t_id=request.session['trainerid']
	trainer=models.Trainer.objects.get(pk=t_id)
	msg=None
	if request.method=='POST':
		form=forms.TrainerProfileForm(request.POST,request.FILES,instance=trainer)
		if form.is_valid():
			form.save()
			msg='Profile has been updated'
	form=forms.TrainerProfileForm(instance=trainer)
	return render(request, 'trainer/profile.html',{'form':form,'msg':msg})

# Notifications
def notifs(request):
	data=models.Notify.objects.all().order_by('-id')
	return render(request, 'notifs.html', {'data':data})

# get all notifications
def get_notifs(request):
	data=models.Notify.objects.all().order_by('-id')
	notifStatus=False
	jsonData=[]
	totalUnread=0
	for d in data:
		try:
			notifStatusData=models.NotifUserStatus.objects.get(user=request.user,notif=d)
			if notifStatusData:
				notifStatus=True
		except models.NotifUserStatus.DoesNotExist:
			notifStatus=False
		if not notifStatus:
			totalUnread=totalUnread+1
		jsonData.append({
				'pk':d.id,
				'notify_detail':d.notify_detail,
				'notifStatus':notifStatus
			})
	# jsonData=serializers.serialize('json', data)
	return JsonResponse({'data':jsonData,'totalUnread':totalUnread})
def mark_read_notif(request):
	notif=request.GET['notif']
	notif=models.Notify.objects.get(pk=notif)
	user=request.user
	models.NotifUserStatus.objects.create(notif=notif,user=user,status=True)
	return JsonResponse({'bool':True})


# Trainer Subscribers
def trainer_subscribers(request):
	trainer=models.Trainer.objects.get(pk=request.session['trainerid'])
	trainer_subs=models.AssignSubscriber.objects.filter(trainer=trainer).order_by('-id')
	return render(request, 'trainer/trainer_subscribers.html',{'trainer_subs':trainer_subs})


# Trainer Payments
def trainer_payments(request):
	trainer=models.Trainer.objects.get(pk=request.session['trainerid'])
	trainer_pays=models.TrainerSalary.objects.filter(trainer=trainer).order_by('-id')
	return render(request, 'trainer/trainer_payments.html',{'trainer_pays':trainer_pays})


# Trainer Change Password
def trainer_changepassword(request):
	msg=None
	if request.method=='POST':
		new_password=request.POST['new_password']
		updateRes=models.Trainer.objects.filter(pk=request.session['trainerid']).update(pwd=new_password)
		if updateRes:
			del request.session['trainerLogin']
			return redirect('/trainerlogin')
		else:
			msg='Something is wrong!!'
	form=forms.TrainerChangePassword
	return render(request, 'trainer/trainer_changepassword.html',{'form':form})


# Trainer Notifications
def trainer_notifs(request):
	data=models.TrainerNotification.objects.all().order_by('-id')
	trainer=models.Trainer.objects.get(id=request.session['trainerid'])
	jsonData=[]
	totalUnread=0
	for d in data:
		try:
			notifStatusData=models.NotifTrainerStatus.objects.get(trainer=trainer,notif=d)
			if notifStatusData:
				notifStatus=True
		except models.NotifTrainerStatus.DoesNotExist:
			notifStatus=False
		if not notifStatus:
			totalUnread=totalUnread+1
		jsonData.append({
			'pk':d.id,
			'notify_detail':d.notif_msg,
			'notifStatus':notifStatus
		})
	return render(request, 'trainer/notifs.html',{'notifs':jsonData,'totalUnread':totalUnread})


# Trainer Messages
def trainer_msgs(request):
	data=models.TrainerMsg.objects.all().order_by('-id')
	return render(request, 'trainer/msgs.html',{'msgs':data})