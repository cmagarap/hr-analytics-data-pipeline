CREATE TABLE work_experience (
experience_id INT PRIMARY KEY,
candidate_id INT,
job_title VARCHAR(255),
company_name VARCHAR(255),
start_date DATE,
end_date DATE,
description TEXT,
FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id)
);

INSERT INTO work_experience (experience_id, candidate_id, job_title, company_name,
start_date, end_date, description)
VALUES
(1, 1, 'Software Engineer', 'TechCorp', '2018-01-01', '2023-06-01', 'Developed software solutions.'),
(2, 2, 'Data Analyst', 'Data Inc', '2019-03-01', '2023-07-01', 'Analyzed data trends.'),
(3, 1, 'Junior Developer', 'CodeFactory', '2015-06-01', '2017-12-31', 'Assisted in development projects.'),
(4, 3, 'IT Consultant', 'Tech Solutions', '2015-04-01', '2018-06-01', 'Advised clients on IT strategies and infrastructure.'),
(5, 2, 'Business Analyst', 'FinancePros', '2014-11-01', '2019-02-22', 'Analyzed business processes and recommended improvements.'),
(6, 1, 'DevOps Engineer', NULL, '2023-06-21', NULL, 'Maintaining cloud infrastructure and CI/CD pipelines.'),
(7, 2, 'Senior Data Analyst', '', '2023-08-05', NULL, NULL),
(8, 3, 'Enterprise Architect', 'MarketCo', '2018-06-18', '2020-03-10', 'Conducted market research and competitor analysis.'),
(9, 3, 'Project Manager', 'NetConnect', '2020-04-01', NULL, 'Designed network infrastructure and maintained security protocols.'),
(10, 4, 'Junior Software Engineer', 'WebDev Solutions', '2014-07-01', '2018-04-25', ''),
(11, 4, 'Software Engineer', 'Innovate Tech', '2018-05-10', '2021-01-28', 'Designed and implemented RESTful APIs for mobile applications.'),
(12, 4, 'Senior Software Engineer', 'Code Masters', '2021-02-13', '2023-06-03', 'Leading a team of developers to build a new cloud-based platform.'),
(13, 4, 'Tech Lead', 'Tech Solutions', '2023-06-15', NULL, 'Providing technical guidance and mentoring junior developers.'),
(14, 5, 'Data Analyst', 'InfoTrode', '2020-06-15', '2022-12-01', 'Worked with structured data, created reports, and performed basic analytics reporting.'),
(15, 5, 'Machine Learning Engineer', 'DigiWiz Inc.', '2023-01-01', '2025-01-23', 'Developed and deployed machine learning models.'),
(16, 6, '', 'Optimum', '2010-11-11', '2014-06-01', 'Handled troubleshooting and basic IT support.'),
(17, 6, 'System Administrator', 'PiedPiper', '2014-07-25', '2020-02-23', 'Managed servers, networks, and IT infrastructure.'),
(18, 6, 'Engineering Lead', 'FlutterBeam', '2020-03-11', '2025-01-30', 'Managed servers, networks, and IT infrastructure.');