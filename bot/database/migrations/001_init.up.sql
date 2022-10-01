CREATE TABLE IF NOT EXISTS songs(
    id VARCHAR(255) UNIQUE PRIMARY KEY,
    title TEXT,
    url TEXT,
    start_time INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS playlists(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER,
    name VARCHAR(30) UNIQUE
);

CREATE TABLE IF NOT EXISTS songs_playlists(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    playlist_id INTEGER REFERENCES playlists(id),
    song_id VARCHAR(255) REFERENCES songs(id)
);

CREATE INDEX songs_playlists_idx ON songs_playlists(song_id, playlist_id);
