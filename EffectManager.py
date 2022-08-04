import Effect

class EffectManager:
    def __init__(self, game):
        self.game = game
        self.effect_list = []

    def add_effect(self, effect):
        self.effect_list.append(effect)

    def update(self):
        next_effect_list = []
        for effect in self.effect_list:
            effect.update()

            if not effect.remove_flag:
                next_effect_list.append(effect)
                
        self.effect_list = next_effect_list
