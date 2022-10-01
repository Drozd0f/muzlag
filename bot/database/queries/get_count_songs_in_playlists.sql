SELECT count(sp.song_id) FROM songs_playlists sp WHERE sp.playlist_id=:playlist_id;
