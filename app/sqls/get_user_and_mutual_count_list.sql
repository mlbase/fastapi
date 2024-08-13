SELECT COUNT(*) AS mutual_count, u.id AS friend_id, u.full_name
FROM (
    SELECT user_id, friend_id FROM friendship WHERE user_id = :user_id
) a
INNER JOIN friendship b ON a.friend_id != b.friend_id and a.friend_id = b.user_id
INNER JOIN api_user u ON u.id = b.friend_id
where u.id != :user_id
GROUP BY u.id, u.full_name
ORDER BY mutual_count DESC;