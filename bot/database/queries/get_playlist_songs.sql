SELECT s.*
FROM songs s
LEFT JOIN songs_playlists sp on s.id = sp.song_id
LEFT JOIN playlists p on p.id = sp.playlist_id
WHERE p.id=:playlist_id
LIMIT :limit OFFSET :offset;
