DELIMITER //
DROP PROCEDURE IF EXISTS GetTopUniversitiesByYear;
CREATE PROCEDURE GetTopUniversitiesByYear(IN keywordId INT)
BEGIN

DECLARE keywordIdVar INT;
SET keywordIdVar = keywordId;

WITH RankedUniversities AS (
    SELECT
        FacUniViewAbr.universityName as universityName,
        COUNT(DISTINCT pub_w_year.publication_id) AS num_pubs,
        MAX(pub_w_year.year) AS year,
        ROW_NUMBER() OVER(PARTITION BY MAX(pub_w_year.year) ORDER BY COUNT(DISTINCT pub_w_year.publication_id) DESC) AS row_num
    FROM
        FacUniViewAbr
    INNER JOIN 
        (SELECT fac_of_pubs.*, publication.year
        FROM publication
        INNER JOIN 
            (SELECT *
                FROM faculty_publication 
                WHERE publication_id IN
                    (SELECT publication_id 
                    FROM publication_keyword 
                    WHERE keyword_id = 
                        (SELECT id 
                        FROM keyword 
                        WHERE id = keywordId))) AS fac_of_pubs
        ON publication.id = fac_of_pubs.publication_id 
        WHERE publication.year >= (SELECT MAX(publication.year)
                                    FROM publication, publication_keyword
                                    WHERE publication.id = publication_keyword.publication_id AND publication_keyword.keyword_id = keywordId)-5) AS pub_w_year
    ON FacUniViewAbr.facultyID = pub_w_year.faculty_id
    GROUP BY FacUniViewAbr.universityName
)
SELECT universityName, num_pubs, year
FROM RankedUniversities
WHERE row_num <= 10
ORDER BY year, num_pubs DESC;

END //

DELIMITER ;