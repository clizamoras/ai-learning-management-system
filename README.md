# AI-Powered Learning Management System

A web-based Learning Management System built with **Django** to help students and teachers manage courses, lessons, assignments, quizzes, and learning progress.

The project also includes an **AI Learning Assistant** using **Ollama and Gemma** to help students understand academic and programming concepts.

## Features

### Student

* Register and login
* Enroll in courses
* Access lessons, videos, and notes
* Submit assignments
* Attempt quizzes
* View results and progress
* Ask questions using the AI assistant

### Teacher

* Create and manage courses
* Add lessons and learning materials
* Create assignments and quizzes
* View student submissions
* Manage announcements and progress

### AI Assistant

* Academic question answering
* Simple explanations
* Programming help
* Conversation history
* Streaming AI responses

## Technologies

* Python
* Django
* Django REST Framework
* HTML, CSS, JavaScript
* SQLite
* Ollama & Gemma
* Git & GitHub

## Run Locally

```bash
git clone https://github.com/clizamoras/ai-learning-management-system.git
cd ai-learning-management-system
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Create a `.env` file containing your Django `SECRET_KEY` and `DEBUG` setting before running the project.

## Project Status

Currently being prepared for deployment.

## Future Improvements

* Cloud deployment
* PostgreSQL database
* Online AI assistant
* Improved analytics and UI
