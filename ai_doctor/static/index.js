document.addEventListener("DOMContentLoaded", () => {
  const homePage = document.getElementById("home_page");
  const doctorsPage = document.getElementById("doctors_page");
  const joinPage = document.getElementById("join_page");
  const doctorPage = document.getElementById("doctor_page");
  const userPage = document.getElementById("userPage");

  const homeButton = document.getElementById("home_button");
  const doctorsButton = document.getElementById("doctors_button");
  const joinButton = document.getElementById("join_button");
  const userButton = document.getElementById("username");

  userButton.addEventListener("click", (e) => {
    e.preventDefault();
    fetch("/getappointments")
      .then((res) => res.json())
      .then((data) => {
        doctorsPage.style.display = "none";
        joinPage.style.display = "none";
        doctorPage.style.display = "none";
        homePage.style.display = "none";
        userPage.style.display = "flex";
        userPage.innerHTML = '<h1 id="appoint">Appointments</h1>';
        data.forEach((appointment) => {
            let isoDate = appointment.date;
            let date = new Date(isoDate);
            let formattedDate = date.toLocaleString('en-US', {
                day: 'numeric', 
                month: 'long', 
                year: 'numeric', 
                hour: '2-digit', 
                minute: '2-digit'
            });
          userPage.innerHTML += `<div class="appointment">
            <div>
                <img src="${appointment.doctor.profile_photo}" alt="" width="100px" style="height: 100px; width: 100px;">
                <p>Dr.${appointment.doctor.name}</p>
                <p style="font-size: smaller; color: rgb(178, 178, 178);">${appointment.doctor.speciality}</p>
            </div>
            <p>${formattedDate}</p>
        </div>`;
        });
      });
  });

  doctorsButton.addEventListener("click", (e) => {
    e.preventDefault();
    fetch("/getdoctors")
      .then((res) => res.json())
      .then((data) => {
        // Clear the content before appending new doctor profiles
        doctorsPage.innerHTML = "";

        // Hide other pages and show the doctors page
        doctorsPage.style.display = "flex";
        joinPage.style.display = "none";
        doctorPage.style.display = "none";
        homePage.style.display = "none";
        userPage.style.display = "none";

        // Loop through each doctor and append to the doctorsPage
        data.forEach((doctor) => {
          doctorsPage.innerHTML += `<div class="item">
                <div class="profile">
                    <img src="${doctor.profile_photo}" alt="profile" width="225px" height="225px">
                    <div class="description">
                        <p>Dr.${doctor.name}</p>
                        <p style="font-size: 12px; color: rgb(115, 115, 115);">${doctor.speciality}</p>
                    </div> 
                </div>
                <a class="see-doctor" id="${doctor.id}" style="cursor: pointer;">Book an appointment</a>
            </div>`;
        });

        // Add event listeners to each "see-doctor" button to fetch individual doctor details
        const doctorButtons = document.querySelectorAll(".see-doctor");
        doctorButtons.forEach((element) => {
          element.addEventListener("click", (e) => {
            const doctorId = e.target.id;
            fetch(`doctorinfo/${doctorId}`)
              .then((res) => res.json())
              .then((data) => {
                // Hide the doctors page and show the selected doctor's details
                doctorsPage.style.display = "none";
                doctorPage.style.display = "flex";

                // Update doctorPage with the fetched doctor details
                document.querySelector(
                  ".doctor-details-container"
                ).innerHTML = `
                    <div class="image-doctor-container">
                        <img src="${data.profile_photo}" alt="" class="square-pic">
                        <div class="doctor-info-container">
                            <h1>Dr. ${data.name}</h1>
                            <p>${data.description}</p>
                        </div>
                        </div>
                        <div class="doctor-address-big-container">
                        <div class="doctor-address-container">
                            <p>Phone: ${data.number}</p>
                            <p>Email: ${data.email}</p>
                            <p>Address: ${data.address}</p>
                        </div>
                            <button class="button-book" id="book-${data.id}" class="book">Book an appointment</button>
                        </div>
                        <p id="if-error"></p>
                    `;

                // Handle the booking process
                const bookButton = document.querySelector(`#book-${data.id}`);
                bookButton.addEventListener("click", (e) => {
                  fetch(`/book/${data.id}`, {
                    method: "POST",
                    headers: {
                      "Content-Type": "application/json",
                      "X-CSRFToken": document
                        .querySelector('meta[name="csrf-token"]')
                        .getAttribute("content"),
                    },
                    body: JSON.stringify({
                      patient: document.getElementById("username").textContent,
                    }),
                  })
                    .then((res) => res.json())
                    .then((data) => {
                      document.getElementById("if-error").innerText =
                        data.error || "Appointment booked successfully!";
                    })
                    .catch((err) => {
                      document.getElementById("if-error").innerText =
                        "Error booking appointment.";
                      console.error("Error:", err);
                    });
                });
              });
          });
        });
      })
      .catch((err) => {
        console.error("Error fetching doctors:", err);
      });
  });

  homeButton.addEventListener("click", (e) => {
    e.preventDefault();
    doctorsPage.style.display = "none";
    joinPage.style.display = "none";
    doctorPage.style.display = "none";
    homePage.style.display = "flex";
    userPage.style.display = "none";
  });

  joinButton.addEventListener("click", (e) => {
    e.preventDefault();
    doctorsPage.style.display = "none";
    joinPage.style.display = "flex";
    doctorPage.style.display = "none";
    homePage.style.display = "none";
    userPage.style.display = "none";
  });

  const join_form = document.getElementById("join_us");
  join_form.addEventListener("submit", (e) => {
    e.preventDefault();
    const formData = new FormData(join_form); // Automatically includes files from the form

    fetch("/createdoctor", {
      method: "POST",
      body: formData, // No need for JSON.stringify when using FormData
      headers: {
        "X-CSRFToken": document
          .querySelector('meta[name="csrf-token"]')
          .getAttribute("content"), // CSRF token from meta tag
      },
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data.message);
        join_form.reset(); // Clear form after submission
      });
  });

  const conversation_form = document.getElementById("conversation");
  conversation_form.addEventListener("submit", (event) => {
    event.preventDefault();
    const message = document.getElementById("message").value;
    fetch("/conversation", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": document
          .querySelector('meta[name="csrf-token"]')
          .getAttribute("content"),
      },
      body: JSON.stringify({ message }),
    })
      .then((res) => res.json())
      .then((data) => {
        document.querySelector(".messages-container").innerHTML += `
                <div class="right-message"><p>${data.message}</p></div>
                <div class="left-message"><p>${data.response}</p></div>`;
        console.log(data.response);
      });
    document.getElementById("message").value = "";
    scrollToBottom();
  });


});
