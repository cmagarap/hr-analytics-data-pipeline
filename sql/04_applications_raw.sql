CREATE TABLE applications (
application_id INT PRIMARY KEY,
candidate_id INT,
job_role VARCHAR(255),
application_date DATE,
status VARCHAR(50),
FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id)
);

INSERT INTO applications (application_id, candidate_id, job_role, application_date, status)
VALUES
(1, 1, 'Senior Software Engineer', '2024-01-15', 'Pending'),
(2, 2, 'Data Scientist', '2024-01-20', 'Interview'),
(3, 3, 'IT Manager', '2024-01-22', 'Rejected'),
(4, 4, 'IT Project Manager', '2024-12-25', 'Accepted'),
(5, 5, 'Data Scientist', '2024-11-26', 'Accepted'),
(6, 6, 'IT Manager', '2024-10-27', NULL),
(7, 3, 'Project Manager', '2020-03-12', 'Accepted'),
(8, 3, 'IT Manager', '2024-10-05', 'Rejected'),
(9, 2, 'Data Analyst', '2023-11-30', 'Accepted');
