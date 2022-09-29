SELECT s.title
FROM songs s
LEFT JOIN songs_playlists sp on s.id = sp.song_id
LEFT JOIN playlists p on p.id = sp.playlist_id
WHERE p.id=:playlist_id ORDER BY sp.id
LIMIT :limit OFFSET :page;
