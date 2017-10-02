from Database import Database
from models.Stats import O_stats
import datetime

class Games(object):
    def __init__(self, date, opponent,):
        self.date = date
        self.opponent = opponent

    def new_stats(self):
        player = input("Enter player name: ")
        receptions = input("Enter the number of receptions: ")
        receiving_yards = input ("Enter the number of receiving yards: ")
        carries = input("Enter the number of carries: ")
        rushing_yards = input("Enter the number of rushing yards: ")
        touchdowns = input("Enter the number of total touchdowns: ")
        stats = O_stats(player = player,
                        receptions = int(receptions),
                        receiving_yards = int(receiving_yards),
                        carries = int(carries),
                        rushing_yards = int(rushing_yards),
                        touchdowns = int(touchdowns),
                        opponent = self.opponent,
                        date = self.date)

        stats.save_to_mongo()

    def get_stats(self):
        return O_stats.from_game(self.opponent, self.date)


    def save_to_mongo(self):
        Database.insert(collection = "Games", data = self.json())

    def json(self):
        return {
            "opponent": self.opponent,
            "date": self.date
        }

    @classmethod
    def from_mongo(cls, opponent, date):
        game_data = Database.find_one(collection = "Games",
                                      query = {"opponent": opponent,
                                               "date": date})

        return cls(opponent = game_data["opponent"],
                   date = game_data["date"])