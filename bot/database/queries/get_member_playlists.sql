SELECT *
FROM playlists
WHERE member_id=:member_id
LIMIT :limit OFFSET :page;
