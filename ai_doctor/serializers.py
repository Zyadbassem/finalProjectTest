from rest_framework import serializers
from .models import CustomUser, Conv, Doctor, Appointment


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class ConvSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conv
        fields = "__all__"


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"


class AppointmentSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()

    class Meta:
        model = Appointment
        fields = "__all__"
