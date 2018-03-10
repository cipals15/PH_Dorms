from django.shortcuts import render
from django.shortcuts import redirect

from .models import Dorm, DormRoom, DormSchool
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from social_django.models import UserSocialAuth

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

# Create your views here.
@login_required
def index(request):
	num_dorms = Dorm.objects.all().count()
	
	num_visits = request.session.get('num_visits',0)
	request.session['num_visits'] = num_visits+1
	
	return render(
		request,
		'index.html',
		context = {'num_dorms':num_dorms,'num_visits': num_visits},
	)

class DormsListView(LoginRequiredMixin, generic.ListView):
	model = Dorm
	paginate_by = 8
	
	def get_queryset(self):
		qs = Dorm.objects.all()
		
		keywords = self.request.GET.get('q')
		if keywords:
			query = SearchQuery(keywords)
			vector = SearchVector('dorm_name','dorm_description','dorm_address','dorm_caretaker','dorm_house_rules','dorm_contact_no','dorm_contact_email')
			qs = qs.annotate(search=vector).filter(search=query)
			qs = qs.annotate(rank=SearchRank(vector, query)).order_by('-rank')
			
		return qs
	
class DormsDetailView(LoginRequiredMixin, generic.DetailView):
	model = Dorm
	
	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['room_numbers'] = self.object.dormroom_set.values_list("id","room_number")
		return context
	
class DormsRoomView(LoginRequiredMixin, generic.ListView):
	model = DormRoom
	
class DormsRoomsDetailView(LoginRequiredMixin, generic.DetailView):
	model = DormRoom
	
	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['images'] = self.object.images.all()
		context['amenities'] = self.object.amenities.all()
		return context
	
class DormSchoolListView(LoginRequiredMixin, generic.ListView):
	model = DormSchool
	
class DormSchoolDetailView(LoginRequiredMixin, generic.DetailView):
	model = DormSchool
	
	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['dorm_list'] = self.object.dorms_list.values_list("id","dorm_name")
		return context
		
@login_required
def settings(request):
	user = request.user
	
	try:
		github_login = user.social_auth.get(provider='github')
	except UserSocialAuth.DoesNotExist:
		github_login = None
		
	try:
		twitter_login = user.social_auth.get(provider='twitter')
	except UserSocialAuth.DoesNotExist:
		twitter_login = None
		
	try:
		facebook_login = user.social_auth.get(provider='facebook')
	except UserSocialAuth.DoesNotExist:
		facebook_login = None
		
	can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())
	
	return render(request, 'settings.html', {
		'github_login': github_login,
		'twitter_login': twitter_login,
		'facebook_login': facebook_login,
		'can_disconnect': can_disconnect
	})
	
def password(request):
	if request.user.has_usable_password():
		PasswordForm = PasswordChangeForm
	else:
		PasswordForm = AdminPasswordChangeForm
		
	if request.method == 'POST':
		form = PasswordForm(request.user, request.POST)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			message.success(request, 'Your password was successfully updated!')
			return redirect('password')
		else:
			message.error(request, 'Please correct the error below.')
	else:
		form = PasswordForm(request.user)
	return render(request, 'password.html', {'form': form})