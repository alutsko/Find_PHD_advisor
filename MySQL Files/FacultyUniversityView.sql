CREATE VIEW FacultyUniversityView AS
SELECT f.id AS faculty_id, 
    f.name AS faculty_name, 
    f.position, 
    f.research_interest, 
    f.email, 
    f.phone, 
    f.photo_url AS faculty_photo_url, 
    u.id AS university_id, 
    u.name AS university_name, 
    u.photo_url AS university_photo_url
FROM faculty f
INNER JOIN university u ON f.university_id = u.id;