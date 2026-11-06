CREATE DATABASE IF NOT EXISTS student_feedback
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE student_feedback;

CREATE TABLE IF NOT EXISTS courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(150) NOT NULL UNIQUE,
    faculty_name VARCHAR(150) NOT NULL
);

CREATE TABLE IF NOT EXISTS feedback_questions (
    question_id INT AUTO_INCREMENT PRIMARY KEY,
    question_text VARCHAR(255) NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS feedback (
    feedback_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    question_id INT NOT NULL,
    rating TINYINT NOT NULL,
    comment_optional VARCHAR(1000) NULL,
    submitted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_feedback_course FOREIGN KEY (course_id)
        REFERENCES courses(course_id),
    CONSTRAINT fk_feedback_question FOREIGN KEY (question_id)
        REFERENCES feedback_questions(question_id),
    CONSTRAINT chk_rating CHECK (rating BETWEEN 1 AND 5),
    INDEX idx_feedback_course_question (course_id, question_id)
);

INSERT IGNORE INTO courses (course_name, faculty_name) VALUES
('Python Programming', 'Faculty A'),
('Database Management Systems', 'Faculty B'),
('Mathematics', 'Faculty C');

INSERT INTO feedback_questions (question_text) VALUES
('How clearly was the subject explained?'),
('How useful were the learning materials?'),
('How engaging were the classes?'),
('How satisfied are you with the course overall?');
