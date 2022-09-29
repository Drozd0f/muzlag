SELECT s.*
FROM songs s
LEFT JOIN songs_playlists sp on s.id = sp.song_id
WHERE sp.playlist_id=:playlist_id AND s.id=:song_id;
