# StudyBuddy - University Collaboration Platform

**Version:** 1.0  
**Author:** Elizabeth Atieno  

---

## Table of Contents
1. [Project Overview](#project-overview)  
2. [Problem Statement](#problem-statement)  
3. [Solution](#solution)  
4. [Features](#features)  
5. [Technologies Used](#technologies-used)  
6. [Database Structure](#database-structure)  
7. [Installation & Setup](#installation--setup)  
8. [Usage](#usage)   

---

## Project Overview
StudyBuddy is a web-based platform that connects university students with peers, mentors, lecturers, and learning resources. The goal is to enhance collaboration, skill development, and academic performance through a centralized system.  

---

## Problem Statement
University students often face difficulties in:  
- Finding study partners with similar courses or skills.  
- Accessing lecturers, practice exercises, and learning tools in a single platform.  
- Discovering internships and collaboration opportunities.  

---

## Solution
StudyBuddy addresses these challenges by providing:  
- **Student Matching**: Find study buddies by course, skills, and university.  
- **Learning Resources**: Access lecturers, practice exercises, internships, and developer tools.  
- **Real-Time Interaction**: Send buddy requests, chat, and filter matches by skills.  
- **Productivity Enhancement**: Centralized environment for learning, networking, and mentorship.  

---

## Features
- User registration and login  
- Profile creation (course, skills, university)  
- Find and match study buddies  
- Send and respond to buddy requests  
- Real-time chat system  
- Access to lecturers and exercises  
- Developer tools and tutorials (Supabase, Cursor AI, MGX, Rork.app, Bolt.new, Claude.ai)  
- Skill-based filtering and premium content options  

---

## Technologies Used
- **Backend**: Python Flask  
- **Frontend**: HTML, CSS, JavaScript  
- **Database**: MySQL  
- **Tools & Integrations**: Supabase, Cursor AI, MGX, Rork.app, Bolt.new, Claude.ai  

---

## Database Structure
### Tables:
- **users**: Stores user credentials.  
- **students**: Stores profile details.  
- **buddy_requests**: Tracks requests between students.  
- **messages**: Handles chat messages.  
- **lecturers**: Stores lecturer information.  
- **exercises**: Stores practice exercises.  
- **companies**: Stores internship/company details.  
- **tools**: Stores developer tools and guides.  

---

## Installation & Setup
1. Clone the repository:  
   ```bash
   git clone <repository-url>
 
## Install required Python packages:
pip install -r requirements.txt

## Set up MySQL database:
1. Create studybuddy_db database.
2. Execute database.sql to create tables and insert sample data.

## Run the Flask app:
python app.py

## Usage
1. Register as a student.
2. Create a profile with course, skills, and university.
3. Find study buddies, send requests, and chat in real-time.
4. Access lecturers, exercises, internships, and developer tools.



