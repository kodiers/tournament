-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Create table Players (store player's info)
CREATE TABLE players (id serial PRIMARY KEY , name text);

-- Create table Matches (store matches info)
CREATE TABLE matches (id serial PRIMARY KEY, player1 INTEGER REFERENCES Players(id), player2 INTEGER REFERENCES Players(id), wins INTEGER REFERENCES Players(id) NULL, completed BOOL NULL );

-- Create view
CREATE VIEW futurematches AS SELECT player1 as id1, player2 as id2 FROM Players JOIN Matches ON Players.id = player1 AND Players.id = player2 WHERE wins = NULL;