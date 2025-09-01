-- Create the main database for the Study Buddy app
CREATE DATABASE studybuddy_db;

-- Switch to the newly created database
USE studybuddy_db;


-- USERS TABLE
-- Stores all registered users (students, potentially admins later)

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,   -
    username VARCHAR(100) UNIQUE NOT NULL,  -- Username, must be unique
    email VARCHAR(100) UNIQUE NOT NULL,     -- Email, must be unique
    password VARCHAR(255) NOT NULL          -- Hashed password for authentication
);


-- STUDENTS TABLE
-- Stores student-specific info like course, skills, and university
-- Linked to 'users' table via user_id

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique ID for each student profile
    user_id INT NOT NULL,               
    course VARCHAR(100) NOT NULL,       -- Student's course
    skills VARCHAR(255),                
    university VARCHAR(100),            -- University name
    FOREIGN KEY (user_id) REFERENCES users(id)
);


-- BUDDY REQUESTS TABLE
-- Tracks buddy requests between students

CREATE TABLE buddy_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,        
    sender_id INT NOT NULL,                  
    receiver_id INT NOT NULL,                   
    status ENUM('pending', 'accepted', 'declined') DEFAULT 'pending', -- Request status
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Timestamp of request
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE
);


-- MESSAGES TABLE
-- Stores chat messages between users

CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,         
    sender_id INT NOT NULL,                   
    receiver_id INT NOT NULL,                  
    content TEXT NOT NULL,                     -- Message content
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Timestamp sent
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE
);


-- LECTURERS TABLE
-- Stores lecturers that students can access for guidance

CREATE TABLE lecturers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,   -- Lecturer's full name
    course VARCHAR(100) NOT NULL, -- Course they teach
    email VARCHAR(100)            -- Optional contact email
);


-- EXERCISES TABLE
-- Stores practice exercises linked to courses

CREATE TABLE exercises (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,      -- Exercise title
    description TEXT,                 -- Details about the exercise
    course VARCHAR(100) NOT NULL,     -- Related course
    link VARCHAR(255)                 -- Link to the exercise
);

-- Insert sample lecturers
INSERT INTO lecturers (name, course, email) VALUES
('Dr. Jane Vivian', 'Computer Science', 'jane.vivian@multimediauniversity.com'),
('Prof. John Smith', 'Sociology', 'john.smith@masenouniversity.com'),
('Dr. Alice Wasama', 'Information Technology', 'alice.wasama@uonuniversity.com'),
('Prof. Michael Otieno', 'Business Management', 'michael.otieno@cooperativeuniversitykenya.com');

-- Insert sample exercises
INSERT INTO exercises (title, description, course, link) VALUES
('Python Basics Quiz', 'Test your Python basics skills', 'Computer Science', 'https://example.com/python-quiz'),
('Sociology Case Study', 'Analyze a sociology scenario', 'Sociology', 'https://example.com/sociology-case'),
('Information Technology Project', 'Complete an IT project task', 'Information Technology', 'https://example.com/it-project'),
('Business Management Simulation', 'Complete a business strategy simulation', 'Business Management', 'https://example.com/business-sim');


-- COMPANIES TABLE
-- Stores companies offering internships or attachments

CREATE TABLE companies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,         -- Company name
    sector VARCHAR(100),                -- Business sector
    contact_email VARCHAR(100),         -- Contact email
    link VARCHAR(255)                   -- Link for more info
);


-- TOOLS TABLE
-- Stores tools referenced in assignment (Supabase, Cursor AI, etc.)

CREATE TABLE IF NOT EXISTS tools (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,         -- Tool name
    access_link VARCHAR(255),           -- Access link
    guide VARCHAR(255)                  -- Tutorial or guide link
);

-- Insert tools from your assignment
INSERT INTO tools (name, access_link, guide) VALUES
('Supabase + Lovable.dev', 'https://supabase.com', 'https://docs.lovable.dev'),
('Lovable + Supabase setup & troubleshooting', 'https://lovable.dev', 'https://docs.lovable.dev'),
('Cursor AI', 'https://www.cursor.ai/', 'Cursor AI Tutorial for Beginners (2025 Edition)'),
('MGX (MetaGPT X)', 'https://mgx.dev', 'See “Build an Image Editor with MGX.Dev” TikTok demo'),
('Rork.app', 'https://rork.app', 'Build iOS & Android Apps Using AI: Rork Tutorial'),
('Bolt.new', 'https://bolt.new', 'Bolt.new tutorial video'),
('Claude.ai', 'https://www.anthropic.com/claude', 'Prompt Engineering with Claude 3 Opus');
