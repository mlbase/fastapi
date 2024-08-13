SELECT COUNT(*) AS mutual_count
FROM (
    SELECT user_id, friend_id FROM friendship WHERE user_id = :user_id
) a
INNER JOIN friendship b ON b.user_id = :checking_id and a.friend_id = b.friend_id
ORDER BY mutual_count DESC;