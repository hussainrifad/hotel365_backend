from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('list', views.HotelViewSet)
router.register('reviews', views.ReviewViewSet)
router.register('bookings', views.BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('reviews/get/<int:hotel_id>/', views.HotelReviewsView.as_view(), name='hotelreview'),

]