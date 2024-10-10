import challonge
import discord


def create_tourney(title, id, tourney_type):
    try:
        challonge.tournaments.create(title, id, tourney_type)
        return f"https://challonge.com/{id}"
        
    except challonge.ChallongeException as e:
        print("Error creating tournament:", e)
        return False
    
def add_participant(id, name):
    try:
        challonge.participants.create(id, name)
        return f"added {name}"
    except challonge.ChallongeException as e:
        return f"{e} so no one was added!"

def bulk_add(id, names):
    try:
        challonge.participants.bulk_add(id, names)
        return f'added {", ".join(names)}'
    except challonge.ChallongeException as e:
        return e
    
def remove_participant(url, name):
    player_list = challonge.participants.index(url)
    print(player_list)
    for i in range(len(player_list)):
        if player_list[i]["name"] == name:
            challonge.participants.destroy(url, player_list[i]["id"])
            return f"removed {name}"
        
    return f"{name} not found in the bracket!"

def delete_bracket(url):
    try:
        challonge.tournaments.destroy(url)
        return "Bracket has been deleted"
    except:
        return "Bracket not found"

def random_seeding(url):
    try:
        challonge.participants.randomize(url)
        return "Seeding has been randomized."
    except:
        return "bracket not found"
    
def entrant_num(url):
    try:
        player_list = challonge.tournaments.show(url)
        return player_list["participants_count"]
    except:
        return "bracket not found"
    
def view_tourney(url):
    return challonge.tournaments.show(url)
    
def display_winner(url):
    match_list = challonge.matches.index(url)
    if get_completed(url):
        winnerID = match_list[-1]["winner_id"]
        winner = challonge.participants.show(url, winnerID)["name"]
        return winner
    else:
        return "TBD"
    
def get_completed(url):
    if challonge.tournaments.show(url)["state"] == "complete":
        return True
    else:
        return False