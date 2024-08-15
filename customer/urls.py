from django.urls import path, include
from .views import CustomerViewSet, CustomerLoginView, RegistrationApiView, CustomerLogoutView, DepositeBalanceView
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('list', CustomerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('registration/', RegistrationApiView.as_view(), name='registration'),
    path('login/', CustomerLoginView.as_view(), name='login'),
    path('logout/', CustomerLogoutView.as_view(), name='logout'),
    path('deposite_balance/', DepositeBalanceView.as_view(), name='deposite_money'),
    path('active/<uid64>/<token>/', views.activate, name='active'),
]