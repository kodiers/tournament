-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Create table Players (store player's info)
CREATE TABLE Players (id serial PRIMARY KEY , name text, wins NUMERIC, loses NUMERIC, total_scores NUMERIC);

-- Create table Matches (store matches info)
CREATE TABLE Matches (id serial PRIMARY KEY, player1 INTEGER REFERENCES Players(id), player2 INTEGER REFERENCES Players(id),
    player1_score NUMERIC, player2_score NUMERIC);

