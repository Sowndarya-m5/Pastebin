CREATE DATABASE pastebin; 

USE pastebin; 

CREATE TABLE pastes ( 
id VARCHAR(20) PRIMARY KEY, 
content TEXT, 
created_at DATETIME, 
expires_at DATETIME, 
max_views INT, 
views_used INT ); 


select * from pastes;