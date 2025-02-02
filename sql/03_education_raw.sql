CREATE TABLE education (
education_id INT PRIMARY KEY,
candidate_id INT,
degree VARCHAR(255),
institution VARCHAR(255),
start_year YEAR,
completion_year YEAR,
FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id)
);

INSERT INTO education (education_id, candidate_id, degree, institution, start_year, completion_year)
VALUES
(1, 1, 'BSc Computer Science', 'University of Sydney', 2010, 2014),
(2, 2, 'BSc Data Science', 'University of Melbourne', 2013, 2018),
(3, 3, 'BSc Information Technology', 'University of Queensland', 2012, 2016),
(4, 4, 'BSc Project Management', 'University of Western Australia', 2011, 2015),
(5, 3, 'MSc IT Management', 'Monash University', 2017, 2019),
(6, 5, 'BSc Data Analytics', 'University of Tasmania', 2010, 2014),
(7, 2, 'MBA Business Analytics', 'University of Melbourne', 2019, 2021),
(8, 6, 'BSc Information Technology', 'Charles Darwin University', 2016, 2020),
(9, 1, 'MSc Cloud Computing', 'University of Sydney', 2021, 2023);
