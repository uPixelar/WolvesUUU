from splash import get_splash

class Game:
    def __init__(self):
        self.winner_text = get_splash()
        self.vol_overall = 1.0
        self.vol_ingame_music = 1.0
        self.vol_menu_music = 1.0
        self.vol_sound_effects = 1.0
    
game = Game()