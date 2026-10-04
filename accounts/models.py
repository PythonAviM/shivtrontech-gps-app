
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# accounts/models.py
import uuid


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    name = models.CharField(max_length=100)

class EmailOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return (timezone.now() - self.created_at).seconds > 300


from django.db import models
from django.contrib.auth.models import User


import uuid

class Device(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="devices")
    name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.device_id   # ✅ this fixes it
    
    def latest_data(self):
    # ✅ ADD THIS
        return self.data.order_by('-timestamp').first()

    
# accounts/models.py
  
class DeviceData(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="data")
    latitude = models.FloatField()
    longitude = models.FloatField()
    speed = models.FloatField()
    timestamp = models.DateTimeField()
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="devices")






# accounts/models.py

class OTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class UserFCMToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.TextField()

    def __str__(self):
        return self.user.username





class Geofence(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius = models.FloatField()  # meters
    is_active = models.BooleanField(default=True)
    notification_enabled = models.BooleanField(default=False)









class AppPinOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.otp}"





















# =====================================================
# SUBSCRIPTION PLANS
# =====================================================

class SubscriptionPlan(models.Model):

    name = models.CharField(max_length=100)

    price = models.IntegerField()

    duration_days = models.IntegerField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# =====================================================
# DEVICE SUBSCRIPTIONS
# =====================================================

class DeviceSubscription(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE
    )

    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.CASCADE
    )

    amount = models.IntegerField()

    start_date = models.DateTimeField(
        auto_now_add=True
    )

    end_date = models.DateTimeField()

    is_active = models.BooleanField(default=True)

    razorpay_payment_id = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )


    last_notification_sent = models.DateTimeField(null=True,blank=True)
	
    def __str__(self):
        return f"{self.device.device_id} - {self.plan.name}"
















class ExpiryNotificationSetting(models.Model):

    notify_before_days = models.IntegerField(
        default=7
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):

        return f"Notify Before {self.notify_before_days} Days"



class ExpiryNotificationTime(models.Model):

    setting = models.ForeignKey(

        ExpiryNotificationSetting,

        on_delete=models.CASCADE,

        related_name="times"
    )

    time = models.TimeField()

    def __str__(self):

        return str(self.time)











# =========================================================
# EXPIRY NOTIFICATION LOG
# =========================================================

class ExpiryNotificationLog(models.Model):

    device = models.ForeignKey(

        Device,

        on_delete=models.CASCADE
    )

    user = models.ForeignKey(

        User,

        on_delete=models.CASCADE
    )

    remaining_days = models.IntegerField()

    title = models.CharField(
        max_length=255
    )

    body = models.TextField()

    status = models.CharField(
        max_length=50,
        default="Pending"
    )

    response = models.TextField(
        null=True,
        blank=True
    )

    sent_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"{self.device.device_id} "
            f"- {self.status}"
        )
