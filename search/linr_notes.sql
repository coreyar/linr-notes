CREATE DATABASE IF NOT EXISTS linr_notes;
CREATE TABLE IF NOT EXISTS linr_notes.searches(
	            search_id INTEGER PRIMARY KEY AUTO_INCREMENT,
	            artist_search BOOLEAN,
	            recording_title_search BOOLEAN,
	            ip_address TEXT);
CREATE TABLE IF NOT EXISTS linr_notes.artist_searches(
				id INTEGER  PRIMARY KEY AUTO_INCREMENT,
				search_id INTEGER,
				search_term TEXT,
				FOREIGN KEY (search_id) REFERENCES searches(search_id));
CREATE TABLE IF NOT EXISTS linr_notes.recording_searches(
				id INTEGER PRIMARY KEY AUTO_INCREMENT,
				search_id INTEGER,
				search_term TEXT,
				FOREIGN KEY (search_id) REFERENCES searches(search_id));

