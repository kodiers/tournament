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
    connection.close()


def deletePlayers():
    """Remove all the player records from the database."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM players;")
    connection.commit()
    connection.close()


def countPlayers():
    """Returns the number of players currently registered."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT('*') FROM players;")
    count = int(cursor.fetchall()[0][0])
    connection.close()
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
    connection.close()




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
    cursor.execute("SELECT id,name, wins, matches FROM standings ORDER BY wins DESC;")
    objects = cursor.fetchall()
    connection.close()
    return objects


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO matches (player1, player2, player1_win) VALUES (%s, %s, TRUE)", (winner, loser, ))
    cursor.execute("INSERT INTO matches (player1, player2, player1_win) VALUES (%s, %s, FALSE)", (loser, winner, ))
    connection.commit()
    connection.close()
 
 
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
    cursor.execute("SELECT players.id, players.name, wins.number as wins FROM players, wins WHERE players.id = wins.id ORDER BY wins DESC;")
    objects = cursor.fetchall()
    connection.close()
    rounds = math.log(len(objects), 2)
    matches = (rounds * len(objects)) / 2    # Calculate matches count
    i = 0
    swisspairings = []
    # Create pairings for each match
    while i < matches:
        player1_id = objects[i][0]
        player1_name = objects[i][1]
        player2_id = objects[i + 1][0]
        player2_name = objects[i + 1][1]
        swisspairings.append((player1_id, player1_name, player2_id, player2_name))
        i += 2
    return swisspairings




