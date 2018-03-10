from django.db import models
from django.urls import reverse

# Create your models here.

class Dorm(models.Model):
	dorm_name = models.CharField(max_length=50, help_text="Enter dorm name")
	dorm_description = models.TextField(max_length=1000, help_text="Enter dorm description")
	dorm_primary_picture = models.ImageField(help_text="Enter dorm primary pic")
	dorm_room_count = models.IntegerField(help_text="Enter no. of rooms")
	dorm_address = models.CharField(max_length=100,help_text="Enter dorm address")
	dorm_caretaker = models.CharField(max_length=50,help_text="Enter caretaker name")
	dorm_contact_no = models.CharField(max_length=50,help_text="Enter dorm contact number")
	dorm_contact_email = models.EmailField(max_length=254,help_text="Enter dorm email")
	dorm_date_added = models.DateTimeField(help_text="Enter Date Dorm was created")
	dorm_availability = models.CharField(max_length=50, help_text="Is dorm available")
	dorm_date_updated = models.DateTimeField(help_text="Enter Date Dorm information was updated")
	dorm_house_rules = models.TextField(max_length=1000, help_text="Enter dorm house rules")
	
	class Meta:
		ordering = ["-dorm_name"]
		
	def get_absolute_url(self):
		return reverse('dorm-detail',args=[str(self.id)])
	
	def __str__(self):
		return self.dorm_name
		
class DormRoom(models.Model):
	room_number = models.CharField(max_length=20, help_text="Enter room number")
	room_maxusers = models.IntegerField(help_text="Enter maximum # of room users")
	room_dorm = models.ForeignKey(Dorm, on_delete=models.CASCADE)
	room_count = models.IntegerField(help_text="Enter # of rooms in this Dorm room")
	room_description = models.TextField(max_length=1000, default=None, null=True, blank=True, help_text="Enter dorm description")
	room_floor = models.CharField(max_length=10, default=None, null=True, blank=True, help_text="Enter the floor this room belongs to")
	room_caretaker = models.CharField(max_length=50, default=None, null=True, blank=True, help_text="Enter room caretaker name")
	room_contact_no = models.CharField(max_length=50,default=None, null=True, blank=True, help_text="Enter room contact number")
	room_contact_email = models.EmailField(max_length=254, default=None, null=True, blank=True, help_text="Enter room email")
	room_date_added = models.DateTimeField(default=None, null=True, blank=True, help_text="Enter Date room was created")
	room_availability = models.CharField(max_length=50, default=None, null=True, blank=True, help_text="Is room available")
	room_date_updated = models.DateTimeField(default=None, null=True, blank=True, help_text="Enter Date Room information was updated")
	room_house_rules = models.TextField(default=None, null=True, blank=True, max_length=1000, help_text="Enter room house rules")
	
	def get_absolute_url(self):
		return reverse('rooms-detail', args=[str(self.id)])
		
	def __str__(self):
		return self.room_number
		
	class Meta:
		ordering = ('room_number',)
		
class DormSchool(models.Model):
	school_name = models.CharField(max_length=50, help_text="Enter the school")
	school_description = models.CharField(max_length=200, null=True, help_text="Enter the school description")
	school_logo = models.ImageField(default=None, null=True, blank=True, help_text="Upload school logo")
	dorms_list = models.ManyToManyField(Dorm)
	
	def get_absolute_url(self):
		return reverse('schools-detail', args=[str(self.id)])
	
	def __str__(self):
		return self.school_name
		
	class Meta:
		ordering = ('school_name',)
		
class DormRoomImage(models.Model):
	dorm_room = models.ForeignKey(DormRoom, on_delete=models.CASCADE, related_name='images')
	dorm_image = models.ImageField(help_text='Upload a room image')
	
class DormRoomAmenities(models.Model):
	dorm_room = models.ForeignKey(DormRoom, on_delete=models.CASCADE, related_name='amenities')
	room_aircon = models.CharField(max_length=50, help_text="Enter Aircon Type")
	room_wifi = models.CharField(max_length=50, help_text="Enter Wifi details")
	room_kitchen = models.CharField(max_length=50, help_text="Enter Kitchen details")
	room_fireextenguisher = models.CharField(max_length=50, help_text="Enter Fire details")
	room_tv = models.CharField(max_length=50, help_text="Enter Fire details")
	room_washing = models.CharField(max_length=50, help_text="Enter Fire details")