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
CREATE TABLE matches (id serial PRIMARY KEY, player1 INTEGER REFERENCES players(id),
  player2 INTEGER REFERENCES players(id), player1_win BOOL);

-- Create view CompletedMatches (store comleted matches info and winners)
CREATE VIEW completed_matches AS SELECT * FROM matches WHERE player1_win = TRUE;

-- Create view wins (store wins count for each player info)
CREATE VIEW wins AS SELECT players.id, COUNT(matches.player2) AS number FROM players
  LEFT JOIN completed_matches as matches ON Players.id = matches.player1 GROUP BY players.id;

-- Create view players_matches (store match count for each player)
CREATE VIEW players_macthes AS SELECT players.id, COUNT (matches.player2) AS number FROM players LEFT JOIN matches
    ON players.id = matches.player1 GROUP BY players.id;

-- Create standings view ( store wins and matches info for each player)
CREATE VIEW standings AS SELECT players.id,players.name, wins.number as wins, players_macthes.number as matches
	FROM players, players_macthes, wins WHERE players.id = wins.id and wins.id = players_macthes.id;
