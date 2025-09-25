from django.urls import path
from .views import track_package, TariffsByCategoryView, HomeRateListView, ContactListView, tracking_details_view, \
    send_message_view, BroadcastMessageListView, BroadcastMessageLatestView
from frontend import admin
from . import views

urlpatterns = [
    path('', HomeRateListView.as_view(), name='home'),
    path('track/', track_package, name='track_package'),
    path('rates/', TariffsByCategoryView.as_view(), name='rates'),
    path('rates/category/<int:pk>/', TariffsByCategoryView.as_view(), name='rates_by_category'),
    path('contacts/', ContactListView.as_view(), name='contacts'),
    path('tracking/', tracking_details_view, name='tracking_details'),
    path('tracking/<str:trackid>/', tracking_details_view, name='tracking_details_by_id'),
    path("send_message/", views.send_message_view, name="send_message"),
    path("api/broadcast/list/", BroadcastMessageListView.as_view(), name="broadcast_list"),
    path("api/broadcast/latest/", BroadcastMessageLatestView.as_view(), name="broadcast_latest"),
]
