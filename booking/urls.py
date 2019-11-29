# from django.conf import Settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views


urlpatterns = [
    url('^$', views.index, name='index'),
    url(r'^search/', views.search_results, name='search_results'),
    url(r'^bus-details/(\d+)', views.bus_details, name='bus_details'),
    url(r'^mobile_payment/(\d+)', views.mobile_payment, name='mobile_payment'),
]
