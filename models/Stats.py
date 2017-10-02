from Database import Database


class O_stats(object):
    def __init__(self, player, receptions, receiving_yards, carries, rushing_yards, touchdowns, opponent, date):
        self.player = player
        self.receptions = receptions
        self.receiving_yards = receiving_yards
        self.carries = carries
        self.rushing_yards = rushing_yards
        self.touchdowns = touchdowns
        self.opponent = opponent
        self.date = date


    def save_to_mongo(self):
        Database.insert(collection = "O_stats",
                        data = self.json())

    def json(self):
        return {
            "player": self.player,
            "receptions": self.receptions,
            "receiving_yards": self.receiving_yards,
            "carries": self.carries,
            "rushing_yards": self.rushing_yards,
            "touchdowns": self.touchdowns,
            "opponent": self.opponent,
            "date": self.date
        }

    @classmethod
    def from_mongo(cls, player, opponent):
        stat_data = Database.find_one(collection = "O_stats", query = {"player": player, "opponent": opponent})
        return cls(
            player = stat_data["player"],
            receptions = stat_data["receptions"],
            receiving_yards = stat_data["receiving_yards"],
            carries = stat_data["carries"],
            rushing_yards = stat_data["rushing_yards"],
            touchdowns = stat_data["touchdowns"],
            opponent = stat_data["opponent"],
            date = stat_data["date"]
        )

    @staticmethod
    def from_game(opponent, date):
        return [s for s in Database.find(collection = "O_stats", query = {"opponent": opponent, "date": date})]
