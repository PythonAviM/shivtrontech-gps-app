# =========================================================
# accounts/scheduler.py
# TEST MODE COMPLETE UPDATED CODE
# =========================================================

from apscheduler.schedulers.background import BackgroundScheduler

from django.utils import timezone

from .models import (
    DeviceSubscription,
    ExpiryNotificationLog,
    UserFCMToken
)

from .views import send_fcm_v1


# =========================================================
# CHECK EXPIRY NOTIFICATIONS
# =========================================================

def check_expiry_notifications():

    try:

        print("🔥 RUNNING EXPIRY SCHEDULER")

        # =================================================
        # GET ALL ACTIVE SUBSCRIPTIONS
        # =================================================

        subscriptions = DeviceSubscription.objects.filter(
            is_active=True
        )

        print(
            "TOTAL SUBSCRIPTIONS =>",
            subscriptions.count()
        )

        # =================================================
        # LOOP ALL SUBSCRIPTIONS
        # =================================================

        for subscription in subscriptions:

            print(
                "DEVICE =>",
                subscription.device.device_id
            )

            remaining_days = (
                subscription.end_date.date()
                - timezone.now().date()
            ).days

            print(
                "REMAINING DAYS =>",
                remaining_days
            )

            # =================================================
            # GET USER TOKENS
            # =================================================

            tokens = UserFCMToken.objects.filter(
                user=subscription.user
            )

            print(
                "TOKENS FOUND =>",
                tokens.count()
            )

            # =================================================
            # SEND NOTIFICATION
            # =================================================

            for token in tokens:

                try:

                    title = "⚠️ GPS Plan Expiring"

                    body = (
                        f"{subscription.device.name} "
                        f"expires in "
                        f"{remaining_days} days."
                    )

                    print("🔥 SENDING FCM")

                    send_fcm_v1(

                        token.token,

                        title,

                        body
                    )

                    print(
                        "✅ FCM SENT SUCCESS"
                    )

                    # =========================================
                    # SAVE SUCCESS LOG
                    # =========================================

                    ExpiryNotificationLog.objects.create(

                        device=subscription.device,

                        user=subscription.user,

                        remaining_days=remaining_days,

                        title=title,

                        body=body,

                        status="Delivered",

                        response="Notification Sent Successfully"
                    )

                    print(
                        "✅ LOG SAVED"
                    )

                except Exception as e:

                    print(
                        "❌ FCM ERROR:",
                        str(e)
                    )

                    # =========================================
                    # SAVE FAILED LOG
                    # =========================================

                    ExpiryNotificationLog.objects.create(

                        device=subscription.device,

                        user=subscription.user,

                        remaining_days=remaining_days,

                        title="⚠️ GPS Plan Expiring",

                        body=body,

                        status="Failed",

                        response=str(e)
                    )

                    print(
                        "❌ FAILED LOG SAVED"
                    )

    except Exception as e:

        print(
            "❌ SCHEDULER ERROR:",
            str(e)
        )


# =========================================================
# START APSCHEDULER
# =========================================================

def start():

    scheduler = BackgroundScheduler()

    scheduler.add_job(

        check_expiry_notifications,

        'interval',

        hours=4
    )

    scheduler.start()

    print("✅ APSCHEDULER STARTED")
