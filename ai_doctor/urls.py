from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("home", views.index, name="index"),
    path("sign", views.sign, name="sign"),
    path("register", views.register, name="register"),
    path("conversation", views.conversation, name="conversation"),
    path("createdoctor", views.join_us, name="joinus"),
    path("doctorinfo/<int:doctor_id>", views.doctor_details, name="doctor_details"),
    path("book/<int:doctor_id>", views.book, name="book"),
    path("getdoctors", views.get_doctors, name="get_doctors"),
    path("getappointments", views.get_appointments, name="get_appointments"),
]
