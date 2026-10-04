
# from django.urls import path
# from .views import SignupAPI, LoginAPI, RequestOTP, VerifyOTP

# urlpatterns = [
#     path('signup/', SignupAPI.as_view()),
#     path('login/', LoginAPI.as_view()),
#     path('request-otp/', RequestOTP.as_view()),
#     path('verify-otp/', VerifyOTP.as_view()),
    
# ]

# # urls.py
# urlpatterns += [
#     path('add-device/', AddDeviceAPI.as_view()),
#     path('my-devices/', MyDevicesAPI.as_view()),
#     path('device-data/<str:device_id>/', DeviceDataListAPI.as_view()),
#     path('device-upload/', DeviceDataAPI.as_view()),  # ESP32
# ]

from .views import upload_location


from django.urls import path
from . import views
from .views import (
    SignupAPI,
    LoginAPI,
    RequestOTP,
    VerifyOTP,
    AddDeviceAPI,
    MyDevicesAPI,
    DeviceDataAPI,
    DeviceDataListAPI,
    SingleDeviceDataAPI,
    LatestLocationAPI,
    AdminRequestOTP,
	CreateGeofenceAPI,
	ToggleGeofenceNotificationAPI,
    AdminVerifyOTP,
GetGeofenceAPI,
LogoutAPI,
UserDevicesAPI,    
SaveFCMTokenAPI,
TestNotificationAPI,
app_pin_send_otp,
app_pin_verify_otp,
get_plans,
create_order,
device_subscription,
payment_success,
payment_history,


)

urlpatterns = [
    path('signup/', SignupAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('request-otp/', RequestOTP.as_view()),
    path('verify-otp/', VerifyOTP.as_view()),

    path('add-device/', AddDeviceAPI.as_view()),
    path('my-devices/', MyDevicesAPI.as_view()),
    path('device-data/<str:device_id>/', DeviceDataListAPI.as_view()),
    path('device-upload/', DeviceDataAPI.as_view()),
    path('device/<str:device_id>/', SingleDeviceDataAPI.as_view()),
    path('device-latest/<str:device_id>/', LatestLocationAPI.as_view()),
    path('admin-request-otp/', AdminRequestOTP.as_view()),
    path('admin-verify-otp/', AdminVerifyOTP.as_view()),
    path('api/location/', upload_location),


    path('user-devices/', UserDevicesAPI.as_view()),
       path('logout/', LogoutAPI.as_view()),

	path('save-fcm-token/', SaveFCMTokenAPI.as_view()),

	 path('test-notification/', TestNotificationAPI.as_view()),



	path('create-geofence/', CreateGeofenceAPI.as_view()),

	path('get-geofence/<str:device_id>/', GetGeofenceAPI.as_view()),
	path('toggle-geofence-notification/', ToggleGeofenceNotificationAPI.as_view()),

	path('app-pin-send-otp/', app_pin_send_otp),
    	path('app-pin-verify-otp/', app_pin_verify_otp),

	path('plans/', get_plans),


	path('create-order/', create_order),

	path('payment-success/', payment_success),

	path('device-subscription/<str:device_id>/',device_subscription),

	path('payment-history/<str:device_id>/',payment_history),







    path("privacy-policy/",views.privacy_policy,name="privacy_policy"),

    path("terms-and-conditions/",views.terms_conditions,name="terms_conditions"),

    path("refund-policy/",views.refund_policy,name="refund_policy"),

    path("shipping-policy/",views.shipping_policy,name="shipping_policy"),

    path("contact-us/",views.contact_us,name="contact_us"),


]






