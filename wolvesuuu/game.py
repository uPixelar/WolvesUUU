from splash import get_splash
from typing import Literal
class Game:
    def __init__(self):
        self.winner_text = get_splash()
        self.vol_overall = 1.0
        self.vol_ingame_music = 0.25
        self.vol_menu_music = 0.25
        self.vol_sound_effects = 1.0
        self.should_count = True
        self.count_phase:Literal["round", "switch"] = "round"
        self.show_cursor = True
    
    def resplash(self):
        self.winner_text = get_splash()
    
game = Game()