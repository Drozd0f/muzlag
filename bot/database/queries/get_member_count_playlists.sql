SELECT count(playlists.id)
FROM playlists
WHERE member_id=:member_id;
