from Database import Database
from models.Games import Games
from models.Stats import O_stats
import datetime
class Menu(object):
    def __init__(self):
        self.games = None
        if self.there_are_games():
            print("Here are all the games in the database.")
        else:
            print("There are currently no games in the database.")
            q = input("Would you like to create one? (y) or (n): ")
            if q == "y":
                self.prompt_user_for_game()
            elif q == "n":
                print("Thank you, and goodbye!")



    def there_are_games(self):
        games = Database.find_one("Games", {})
        if games is not None:
            self.games = Games.from_mongo(games["opponent"],
                                          games["date"])
            return True
        else:
            return False


    def prompt_user_for_game(self):
        opponent = input("Enter the opposing team name: ")
        date = input ("Enter the date of the game in DDMMYYY")
        date = datetime.datetime.strptime(date, "%d%m%Y")
        game = Games(opponent = opponent,
                         date = date)

        game.save_to_mongo()
        self.games = game
        self.prompt_user_for_stats()


    def list_games(self):
        games = Database.find("Games", {})

        for g in games:
            print("Opponent: {}, Date: {}.".format(g["opponent"],
                                                  g["date"]))

    def select_game(self):
        print("Which game would you like to view?")
        opponent = input("Enter the name of the opposing team: ")
        d = input("Enter the date (DDMMYYYY): ")
        date = datetime.datetime.strptime(d, "%d%m%Y")
        gam = Games(opponent = opponent,
                     date = date)
        self.games = gam
        game = Games.from_mongo(opponent, date)
        stats = game.get_stats()
        for s in stats:
            print("Player: {}, "
                  "Opponent: {}, "
                  "Date: {}, "
                  "Receptions: {}, "
                  "Receiving_yards: {}, "
                  "YPR: {}, "
                  "Carries: {}, "
                  "Rushing_yards: {}, "
                  "YPC: {}, "
                  "Touchdowns: {}, "
                  .format(s["player"],
                          s["opponent"],
                          s["date"],
                          s["receptions"],
                          s["receiving_yards"],
                          (s["receiving_yards"]/s["receptions"]),
                          s["carries"], s["rushing_yards"],
                          (s["rushing_yards"]/s["carries"]),
                          s["touchdowns"],))

        self.prompt_user_for_stats()



    def prompt_user_for_stats(self):
        stat_prompt = input("Would you like to enter new game stats? yes (y) or no (n): ")
        if stat_prompt == "y":
            self.games.new_stats()
        elif stat_prompt == "n":
            print("Thank you for viewing!")



    def run_menu(self):
        self.list_games()
        game_prompt = input("Would you like to add a new game? Yes (y), No (n):")
        if game_prompt == "y":
            self.prompt_user_for_game()
        elif game_prompt == "n":
            self.select_game()


