from django.contrib import admin
from .models import Dorm, DormRoom, DormSchool, DormRoomImage, DormRoomAmenities

# Register your models here.
class DormAdmin(admin.ModelAdmin):
	list_display = ('dorm_name','dorm_room_count','dorm_caretaker','dorm_contact_no','dorm_availability')
	list_filter = ('dorm_room_count','dorm_caretaker','dorm_availability','dorm_date_added')
	
	fieldsets = (
		(None, {'fields': ('dorm_name', 'dorm_description', 'dorm_primary_picture', 'dorm_room_count')}),
		('Contact Details', {'fields': ('dorm_address','dorm_caretaker','dorm_contact_no','dorm_contact_email')}),
		('Date',{'fields': ('dorm_date_added','dorm_availability','dorm_date_updated')}),
		('Others',{'fields': ('dorm_house_rules',)}),
	)

class RoomImageInline(admin.TabularInline):
	model = DormRoomImage
	extra = 3
	
class RoomAmenitiesInline(admin.TabularInline):
	model = DormRoomAmenities
	extra = 1
	
class RoomAdmin(admin.ModelAdmin):
	list_display = ('room_number','room_maxusers','room_count')
	inlines = [ RoomImageInline, RoomAmenitiesInline, ]
	
admin.site.register(Dorm, DormAdmin)
admin.site.register(DormRoom, RoomAdmin)
admin.site.register(DormSchool)