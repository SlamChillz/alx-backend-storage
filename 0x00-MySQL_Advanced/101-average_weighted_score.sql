-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers
-- that computes and store the average weighted score for all students.
DROP PROCEDURE IF EXISTS `ComputeAverageWeightedScoreForUsers`;

DELIMITER |
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
	DECLARE i INT;
	DECLARE n INT;
	DECLARE d INT;
	SELECT COUNT(*) FROM users INTO n;
	SET i = 0;
	WHILE i < n DO
		SELECT id INTO d FROM users LIMIT i, 1;
		UPDATE users SET average_score = (
			SELECT SUM(x.score * x.weight) / SUM(x.weight)
			FROM (
				SELECT c.score, p.weight 
				FROM corrections c
				LEFT JOIN projects p ON c.project_id = p.id
				WHERE c.user_id = d
			) x
		) WHERE id = d;
		SET i = i + 1;
	END WHILE;
END;
|

DELIMITER ;
