CREATE VIEW `FacUniViewAbr` AS

SELECT faculty.id AS facultyID, university.id AS universityID, university.name AS universityName
FROM faculty
INNER JOIN university
ON faculty.university_id = university.id