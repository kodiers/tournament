#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import math


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM matches;")
    connection.commit()


def deletePlayers():
    """Remove all the player records from the database."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM players;")
    connection.commit()


def countPlayers():
    """Returns the number of players currently registered."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT('*') FROM players;")
    count = int(cursor.fetchall()[0][0])
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO players (name) VALUES (%s);", (name,))
    connection.commit()




def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    connection = connect()
    cursor = connection.cursor()
    num_players = countPlayers()
    cursor.execute("SELECT id, name FROM players;")
    players = cursor.fetchall()
    rounds = math.log(num_players, 2)
    matches = (rounds * num_players) / 2
    i = 0
    while i < matches:
        p1 = players[i][0]
        if i + 1 < len(players):
            p2 = players[i + 1][0]
        if p1 == p2:
            p2 = players[0][0]
        cursor.execute("INSERT INTO matches (player1, player2, wins) VALUES (%s, %s, NULL);", (p1, p2, ))
        connection.commit()
        i += 1
    cursor.execute("SELECT players.id as id, name, COUNT (matches.wins) as wins, COUNT (matches.completed = TRUE ) as matches FROM players JOIN matches ON players.id = matches.player1 OR players.id = matches.player2 GROUP  BY players.id ORDER BY Wins;")
    objects = cursor.fetchall()
    return objects


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("UPDATE matches SET wins = %s, completed = TRUE WHERE player1 = %s AND player2 = %s;", (winner, winner, loser))
    connection.commit()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT id1, players.name as name1, id2,  players.name as name2 FROM futurematches JOIN players ON id1 = players.id, id2 = players.id;")
    objects = cursor.fetchall()
    return objects




