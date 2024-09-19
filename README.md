# AI DOCTOR

AI Doctor is a web application designed to help users assess their health concerns through an AI-powered assistant. Whether you're experiencing a headache, stomachache, or even recovering from an injury, AI Doctor allows you to describe your symptoms and receive recommendations. The AI will analyze the problem and suggest if it’s necessary to consult a doctor. If a consultation is recommended, the app will provide a list of doctors along with the ability to book an appointment directly through the website. The platform is also open to doctors who want to join and serve the community.


## Distinctiveness and Complexity
### Distinctiveness:
This project is distinct because it goes beyond the typical scope of social media or e-commerce platforms seen in other projects. AI Doctor is a unique web application that integrates AI-powered health suggestions with a doctor booking system. Unlike a typical social network, this project focuses on healthcare and well-being, using natural language processing (NLP) and AI to determine the best course of action for users based on their symptoms. Furthermore, this is not an e-commerce website, as the core functionality revolves around healthcare consultation, not transactions.
### Complexity:-
1. AI Integration: The web application utilizes a machine learning API (Gemini API) to process user input and make decisions based on the symptoms described.
2. Django Models: The back-end employs several models, including ones for Users, Doctors, Appointments, and Symptoms, to manage and store data.
3. JavaScript: The front-end involves JavaScript to enhance the interactivity of the user interface. For instance, it dynamically updates doctor suggestions and provides feedback based on user input.
4. Mobile Responsiveness: The entire application is designed to be mobile-responsive, ensuring that users on any device can access it comfortably.
5. API Integration: It pulls from a third-party API for intelligent doctor recommendations, ensuring the project is both informative and functional.

## File Structure and Contents
- manage.py: Django’s command-line utility for administrative tasks.
- finalproject/: Main project directory, containing the settings and configuration files for the Django project.
- settings.py: The main settings file, including configurations for API keys and databases.
- urls.py: URL declarations that route to the appropriate views.
- doctor_app/: Django app that handles core functionality.
- models.py: Contains models for Users, Doctors, Appointments, and Symptoms.
- views.py: Handles the core logic, including interacting with the AI API for symptom analysis and managing appointment bookings.
- templates: HTML templates for the app's front-end.
- static: CSS, JavaScript, and image files for styling and client-side functionality.
- requirements.txt: Python packages required for the project.
- README.md: Documentation for the project.

## how to run the application
1. ##### Clone the Repository from GitHub
Use the git clone command to clone the repository to your local machine. Replace USERNAME with your GitHub username in the command: 
- git clone https://github.com/me50/Zyadbassem.git

2. ##### Switch to the Correct Branch
After cloning the repository, navigate into the project directory and switch to the correct branch: 
cd Zyadbassem
- git checkout web50/projects/2020/x/capstone

3. ##### Create and Activate a Virtual Environment
To create a virtual environment for the project (optional but recommended), run the following command:
- python3 -m venv venv  
source venv/bin/activate (windows)

4. ##### Install Required Packages
Next, install all the required dependencies listed in the requirements.txt file:
- pip3 install -r requirements.txt

5. ##### Set Up Environment Variables
Ensure that your project has the necessary environment variables. If you're using a .env file to store your API keys and settings, create it in the root directory of the project:
- GEMINI_API_KEY=your_gemini_api_key_here

6. ##### Run Migrations
To apply the necessary migrations (create the database tables), run the following command:
- python3 manage.py migrate

7. ##### Run the Development Server
Finally, you can start the Django development server by running:
- python3 manage.py runserver