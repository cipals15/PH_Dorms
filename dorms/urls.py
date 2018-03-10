from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('list/', views.DormsListView.as_view(), name='dorms'),
	path('list/<int:pk>', views.DormsDetailView.as_view(), name='dorm-detail'),
	path('rooms/', views.DormsRoomView.as_view(), name='rooms'),
	path('rooms/<int:pk>', views.DormsRoomsDetailView.as_view(), name='rooms-detail'),
	path('schools/', views.DormSchoolListView.as_view(), name='schools'),
	path('schools/<int:pk>', views.DormSchoolDetailView.as_view(), name='schools-detail'),
]