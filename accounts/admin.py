from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import (
    SubscriptionPlan,
    DeviceSubscription
)
from .models import UserProfile, EmailOTP
from .models import (
    ExpiryNotificationSetting,
    ExpiryNotificationTime
)



from .models import UserFCMToken

from .models import Device, DeviceData 

from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone','message', 'created_at')

admin.site.register(Contact, ContactAdmin)
# Show profile inside User
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)


# unregister default User
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# register other models
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'phone')


@admin.register(EmailOTP)
class EmailOTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp', 'created_at')







class DeviceDataInline(admin.TabularInline):
    model = DeviceData
    extra = 0



# accounts/admin.py
from django.utils.safestring import mark_safe

class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'user', 'show_map')

    def show_map(self, obj):
        data = obj.latest_data()
        if not data:
            return "No location data"

        return mark_safe(f"""
            <div id="map-{obj.id}" style="height:300px;"></div>

            <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css"/>
            <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>

            <script>
                setTimeout(function() {{
                    var lat = {data.latitude};
                    var lon = {data.longitude};

                    var map = L.map('map-{obj.id}').setView([lat, lon], 15);

                    L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                        maxZoom: 19
                    }}).addTo(map);

                    var marker = L.marker([lat, lon]).addTo(map)
                        .bindPopup("Loading address...");

                    // Fetch address (Reverse Geocoding)
                    fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${{lat}}&lon=${{lon}}`)
                    .then(res => res.json())
                    .then(result => {{

                        var address = result.display_name || "Address not found";

                        var popupContent = `
                            <b>Device:</b> {obj.device_id}<br>
                            <b>Speed:</b> {data.speed} km/h<br>
                            <b>Address:</b> ${{address}}<br><br>
                            <a href="https://www.google.com/maps?q=${{lat}},${{lon}}" target="_blank">
                                Open in Google Maps
                            </a>
                        `;

                        marker.bindPopup(popupContent);
                    }});

                }}, 100);
            </script>
        """)

    show_map.short_description = "Live Location"
admin.site.register(Device, DeviceAdmin)

# class DeviceDataAdmin(admin.ModelAdmin):
#     list_display = ('device', 'latitude', 'longitude', 'speed', 'timestamp')

from rangefilter.filters import DateTimeRangeFilter

# accounts/admin.py

class DeviceDataAdmin(admin.ModelAdmin):
    list_display = ('device', 'get_user', 'latitude', 'longitude', 'speed', 'timestamp')

    list_filter = ('device', 'device__user', 'timestamp')
    search_fields = ('device__device_id', 'device__user__username', 'device__user__email')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('device__user')

    def get_user(self, obj):   # ✅ MUST be inside class
        return obj.device.user

    get_user.short_description = "User"
admin.site.register(DeviceData, DeviceDataAdmin)





@admin.register(UserFCMToken)
class UserFCMTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token')



admin.site.register(SubscriptionPlan)
admin.site.register(DeviceSubscription)













admin.site.register(ExpiryNotificationSetting)

admin.site.register(ExpiryNotificationTime)



from .models import ExpiryNotificationLog

admin.site.register(
    ExpiryNotificationLog
)
