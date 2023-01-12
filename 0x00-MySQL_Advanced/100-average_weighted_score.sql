-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser
-- that computes and store the average weighted score for a student.
DROP PROCEDURE IF EXISTS `ComputeAverageWeightedScoreForUser`;

DELIMITER |
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
	UPDATE users SET average_score = (
		SELECT SUM(x.score * x.weight) / SUM(x.weight)
		FROM (
			SELECT c.score, p.weight 
			FROM corrections c
			LEFT JOIN projects p ON c.project_id = p.id
			WHERE c.user_id = user_id
		) x
	) WHERE id = user_id;
END;
|

DELIMITER ;
