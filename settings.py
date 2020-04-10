import pathlib
import pickle

SETTINGS_FILE = pathlib.Path.home().joinpath(".azurbot")


class Settings:
    mode: str
    boss: int
    swap: int
    start_swap: bool
    start_lab: bool
    fight: bool

    def __init__(self):
        # try load settings
        if SETTINGS_FILE.exists():
            if ask("Use old settings [y/n]", "n")[0] == "y":
                self.__dict__.update(pickle.loads(SETTINGS_FILE.read_bytes()).__dict__)
                return

        # configuration
        self.mode = ask("Select mode [Level, Event, Collect, Screen]", "l")[0]
        if self.mode == "l" or self.mode == "e":
            self.swap = int(ask("Battles before swap [5]", "5"))
            self.boss = int(ask("Battles before boss [5]", "5"))
            self.start_swap = ask("Swap on start [n]", "n")[0] == "y"
            self.fight = ask("Use AI [n]", "n")[0] == "y"
        else:
            self.swap = 5
            self.boss = 5
            self.start_swap = False
            self.fight = False

        if self.mode != "s":
            self.start_lab = ask("Start lab [n]", "n")[0] == "y"

        # save settings
        SETTINGS_FILE.write_bytes(pickle.dumps(self, protocol=pickle.HIGHEST_PROTOCOL))

    def __repr__(self):
        return f"Settings({self.mode}, {self.boss}, {self.swap}, {self.start_swap}, {self.fight})"


def ask(quest: str, default: str = "") -> str:
    print(quest, end=": ", flush=True)
    inp = input().lower().strip()
    if len(inp) < 1:
        return default
    return inp
