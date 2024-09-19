from django.shortcuts import render, HttpResponseRedirect, HttpResponse
import google.generativeai as genai
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, Conv, Doctor, Appointment
from .serializers import (
    CustomUserSerializer,
    ConvSerializer,
    DoctorSerializer,
    AppointmentSerializer,
)
from django.contrib import messages
from django.conf import settings

api_key = settings.GEMINI_API_KEY
# Get all doctors and format the list to include both name and specialty
doctor_list = [
    f"{doctor.name} (Specialty: {doctor.speciality})" for doctor in Doctor.objects.all()
]
doctor_list_str = ", ".join(doctor_list)
genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=f"You are an advanced medical expert with a deep understanding of various health conditions, treatments, and medical advice. Your primary role is to provide concise, accurate, and evidence-based answers to health-related queries. "
    "When users ask questions regarding symptoms, treatments, medications, or any other health-related concerns, you should offer well-informed guidance and suggest appropriate next steps. If necessary, advise users to consult a specific type of healthcare professional based on their inquiry. "
    "It is crucial that you remain within the scope of medical expertise and avoid providing advice or information on non-medical topics. In situations where users ask questions unrelated to health or seek general advice outside the realm of medical care, respond with the following statement: "
    "'I'm sorry, but I can only answer medical questions.' This ensures that all interactions remain focused on delivering valuable and relevant medical advice. Remember to uphold the highest standards of professionalism and accuracy in all responses."
    f"If the system finds the user needing a doctor, suggest one of these doctors: {doctor_list_str}.",
)


# done editing
def index(request):
    # check if the user is signed in
    if not request.session.get("username"):
        return HttpResponseRedirect("sign")

    return render(
        request,
        "ai_doctor/index.html",
        {
            "username": request.session.get("username"),
        },
    )


# done editing
@api_view(["GET"])
def doctor_details(request, doctor_id):
    # get doctor details
    doctor_info = Doctor.objects.filter(pk=doctor_id).first()
    if doctor_info is None:
        return Response("doctor doesn't exist")

    # push info
    return Response(DoctorSerializer(doctor_info).data)


# done editing
def sign(request):
    # if the user signs in
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # checking user input
        if not username or not password:
            messages.error(request, "Incorrect username or password")
            return HttpResponseRedirect("sign")

        # get the user from db and check it
        checker = CustomUser.objects.filter(username=username).exists()
        if checker:
            checker = CustomUser.objects.filter(username=username).first()
        else:
            messages.error(request, "Incorrect username or password")
            return HttpResponseRedirect("sign")

        # check the user password
        if checker.check_password(password):
            request.session["username"] = username
            return HttpResponseRedirect("home")
        messages.error(request, "Incorrect username or password")
        return HttpResponseRedirect("sign")

    # if user access via get
    return render(request, "ai_doctor/sign.html", {"sign": True})


# done editing
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        passCon = request.POST.get("passwordCon")
        if (
            not username
            or not email
            or not password
            or not passCon
            or passCon != password
        ):
            messages.error(request, "Incorrect input")
            return HttpResponseRedirect("register")

        user_checker = CustomUser.objects.filter(username=username).exists()
        if user_checker:
            messages.error(request, "user already exist")
            return HttpResponseRedirect("sign")

        user_creator = CustomUser(username=username, email=email)
        user_creator.set_password(password)
        user_creator.save()
        request.session["username"] = username
        return HttpResponseRedirect("home")

    return render(request, "ai_doctor/register.html", {"register": True})


def logout(request):
    # Remove username from session
    request.session.pop("username", None)  # Use pop to avoid key error
    return HttpResponseRedirect("sign")


# done editing
@api_view(["POST"])
def conversation(request):
    # get the data posted
    data = request.data

    # Access the raw Django request object from the DRF request
    django_request = request._request

    # Retrieve previous conversation from session or create an empty list if not found
    previous_responses = django_request.session.get("conversation_history", [])

    # Initialize chat session with the previous history
    chat_session = model.start_chat(history=previous_responses)

    # Generate a new response using the Gemini API
    res = chat_session.send_message(data["message"])

    # Add the new user and model messages to the conversation history
    previous_responses.append({"role": "user", "parts": [data["message"]]})
    previous_responses.append({"role": "model", "parts": [res.text]})

    # Save the updated conversation history back to the session
    django_request.session["conversation_history"] = previous_responses
    django_request.session.modified = (
        True  # Ensure session is marked as modified to save
    )

    return Response(
        {
            "message": data["message"],
            "response": res.text,
            "conversation_history": previous_responses,
        }
    )


# done editing
@api_view(["POST"])
def book(request, doctor_id):
    # get the doctor info
    doc = Doctor.objects.filter(pk=doctor_id).first()
    if doc is None:
        return Response({"error": "doctor doesn't exist"})

    # get the patient
    patient = CustomUser.objects.filter(username=request.data.get("patient")).first()
    if patient is None:
        return Response({"error": "please sign in"})

    # check if the appointment is already booked
    if Appointment.objects.filter(patient=patient, doctor=doc).exists():
        return Response({"error": "you already booked"})

    # create a new appontment
    appointment = Appointment(patient=patient, doctor=doc)
    appointment.save()
    return Response({"error": "done"})


# done editind
@api_view(["POST"])
def join_us(request):
    # Handle form data and file uploads
    if request.method == "POST":
        data = request.POST  # Use request.POST for form data
        profile_photo = request.FILES.get("image")  # Use request.FILES for file upload

        # Print the received data for debugging
        print("Form data:", data)
        print("File data:", profile_photo)

        # Create the doctor object
        doc_creator = Doctor(
            name=data.get("name"),
            email=data.get("email"),
            speciality=data.get("speciality"),
            address=data.get("address"),
            number=data.get("number"),
            profile_photo=profile_photo,  # Assign the uploaded file to profile_photo
        )
        doc_creator.save()

        return Response("Doctor created successfully", status=201)

    return Response("Invalid request method", status=400)


@api_view(["GET"])
def get_doctors(request):
    try:
        # Fetch all doctor records
        doctors = Doctor.objects.all()

        # Serialize the doctor data
        serializer = DoctorSerializer(doctors, many=True)

        # Return the serialized data
        return Response(serializer.data, status=200)

    except Exception as e:
        # Return an error message in case of failure
        return Response({"error": str(e)}, status=500)


@api_view(["GET"])
def get_appointments(request):
    try:
        # Fetch all doctor records
        appointments = Appointment.objects.filter(
            patient=CustomUser.objects.get(username=request.session.get("username"))
        ).order_by("-date")

        # Serialize the doctor data
        serializer = AppointmentSerializer(appointments, many=True)
        # Return the serialized data
        return Response(serializer.data, status=200)

    except Exception as e:
        # Return an error message in case of failure
        return Response({"error": str(e)}, status=500)
