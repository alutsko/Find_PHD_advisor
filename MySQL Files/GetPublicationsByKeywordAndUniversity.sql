DELIMITER //

CREATE PROCEDURE GetPublicationsByKeywordAndUniversity(IN selectedKeywordId INT, IN selectedUniversityId INT)
BEGIN
    DECLARE keywordIdVar INT;
    DECLARE universityIdVar INT;
    SET keywordIdVar = selectedKeywordId;
    SET universityIdVar = selectedUniversityId;

    SELECT pubs_w_facId.title, pubs_w_facId.venue, pubs_w_facId.year, group_concat(FacUniViewAbr.faculty_name separator ', ') AS authors
    FROM (
        SELECT faculty_id, faculty_name, university_id, university_name 
    	FROM FacultyUniversityView 
        WHERE university_id = universityIdVar
    ) AS FacUniViewAbr
    INNER JOIN (
        SELECT faculty_publication.faculty_id, publications_w_scores.*
    	FROM faculty_publication
    	INNER JOIN (
            SELECT publication.id AS publication_id, title, venue, year, num_citations, score
    		FROM publication
    		INNER JOIN (
                SELECT publication_id, score 
    			FROM publication_keyword 
                WHERE keyword_id = keywordIdVar
            ) AS scores
    		ON publication.id = scores.publication_id
        ) AS publications_w_scores
    	ON faculty_publication.publication_id = publications_w_scores.publication_id
    ) AS pubs_w_facId
    ON FacUniViewAbr.faculty_id = pubs_w_facId.faculty_id
    GROUP BY pubs_w_facId.publication_id
    ORDER BY max(pubs_w_facId.score) DESC
    LIMIT 10;
END //

DELIMITER ;