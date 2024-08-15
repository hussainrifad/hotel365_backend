from rest_framework import serializers
from .models import Customer
from django.contrib.auth.models import User
import re


class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    class Meta:
        model = Customer
        fields = '__all__'

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True)
    age = serializers.IntegerField(required=True)
    address = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    birth_date = serializers.DateField()
    
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'confirm_password',
            'age',
            'address',
            'phone',
            'birth_date',
            ]

    def create(self, validated_data):
        username = validated_data['username']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        email = validated_data['email']
        password = validated_data['password']
        confirm_password = validated_data['confirm_password']
        phone = validated_data['phone']
        address = validated_data['address']
        age = validated_data['age']
        birth_date = validated_data['birth_date']

        if password != confirm_password:
            raise serializers.ValidationError({'error' : 'password does not matched'})
        if validate_password(password) == False:
            raise serializers.ValidationError({'error' : 'password must contains one upper letter, one lower letter, one digit, one special character and length should be 8'})
        if User.objects.filter(email=email):
            raise serializers.ValidationError({'error' : 'email already exist'})

        user = User.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save()

        customer = Customer.objects.create(
            user=user,
            address=address,
            age=age,
            phone=phone,
            birth_date=birth_date,
            balance=0,
        )
        return customer


class CustomerLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password']


# password validation
password_pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
password_regex = re.compile(password_pattern)
def validate_password(password):
    if password_regex.fullmatch(password):
        return True
    return False


class DepositeBalanceSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        model = Customer
        fields = ['amount']
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Deposit amount must be greater than zero.")
        return value