from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .serializers import HotelSerializer, ReviewSerializer, BookingSerializer
from .models import Hotel, Review, Booking
from django.core.mail import send_mail
from django.conf import settings
from customer.models import Customer
from rest_framework.response import Response
from datetime import datetime
from rest_framework.exceptions import ValidationError
from rest_framework import status

class HotelViewSet(ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        customer = serializer.validated_data['customer']
        hotel = serializer.validated_data['hotel']

        if customer.balance < hotel.price:
            raise ValidationError("Insufficient balance to complete the booking.")

        if serializer.is_valid():
            customer.balance -= hotel.price
            hotel.rooms -= 1
            hotel.save()
            customer.save()
            booking = serializer.save()
            subject = 'Booking successfully done'
            message = f'Hello Mr. {customer.user.first_name}. your book has been done at {booking.created_at}'
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, message, email_from, [customer.user.email])
            return Response({'success':'booking confirmed'})
        return Response(serializer.errors)

class HotelIsBooked(APIView):
    def get(self, request, hotel_id, user_id):
        
        is_booked = Booking.objects.filter(hotel_id=hotel_id, customer_id=user_id).exists()

        if is_booked:
            return Response({'booked': True}, status=status.HTTP_200_OK)
        else:
            return Response({'booked': False}, status=status.HTTP_200_OK)
    
class HotelReviewsView(APIView):
    
    def get(self, request, hotel_id):
        try:
            hotel = Hotel.objects.get(pk=hotel_id)
        except Hotel.DoesNotExist:
            return Response({'error': 'Hotel not found'}, status=status.HTTP_404_NOT_FOUND)
        
        reviews = hotel.reviews.all() 
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CustomerBookingList(APIView):
    
    def get(self, request, user_id):
        try:
            customer = Customer.objects.get(id=user_id)
        except Customer.DoesNotExist:
            customer = None
        
        if customer is not None:
            list = Booking.objects.filter(customer=customer)
            print(list[0].customer.balance)
            serialize = BookingSerializer(list, many=True)
            return Response(serialize.data)
        return Response([])