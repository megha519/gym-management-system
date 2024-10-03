from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# from gym_mang_syst.settings import MEDIA_ROOT


from . import views
urlpatterns = [
    path('',views.home, name='home'),
    path('pagedetail/<int:id>',views.page_detail, name='pagedetail'),
    path('terms/<int:id>',views.page_detail, name='terms'),
    path('privacy/<int:id>',views.page_detail, name='privacy'),
    path('faq',views.faq_list, name='faq'),
    path('enquiry',views.enquiry_list, name='enquiry'),
    path('gallery',views.gallery, name='gallery'),
    path('gallerydetail/<int:id>',views.gallery_detail, name='gallery_detail'),
    path('pricing',views.pricing, name='pricing'),
    path('accounts/signup',views.signup,name='signup'),
    path('checkout/<int:plan_id>',views.checkout,name='checkout'),
    path('checkout_session/<int:plan_id>',views.checkout_session,name='checkout_session'),
    path('pay_success',views.pay_success,name='pay_success'),
	path('pay_cancel',views.pay_cancel,name='pay_cancel'),
    # User Dashboard Section Start
	path('userdashboard',views.user_dashboard,name='userdashboard'),
	path('updateprofile',views.update_profile,name='updateprofile'),
    # Trainer Login
	path('trainerlogin',views.trainerlogin,name='trainerlogin'),
    path('trainerlogout',views.trainerlogout,name='trainerlogout'),
    path('trainerdashboard',views.trainerdashboard,name='trainerdashboard'),
    path('trainer_profile',views.trainer_profile,name='trainer_profile'),
    path('trainer_subscribers',views.trainer_subscribers,name='trainer_subscribers'),
    path('trainer_payments',views.trainer_payments,name='trainer_payments'),
    path('trainer_changepassword',views.trainer_changepassword,name='trainer_changepassword'),
    path('trainer_notifs',views.trainer_notifs,name='trainer_notifs'),
    # Notifications
	path('notifs',views.notifs,name='notifs'),
    path('get_notifs',views.get_notifs,name='get_notifs'),
    path('mark_read_notif',views.mark_read_notif,name='mark_read_notif'),
    #msgs
    path('messages',views.trainer_msgs,name='messages'),

    

    

    
    
] 
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)