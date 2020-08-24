from .base_warrior_info import BaseWarriorInfo
from app.configurations.colors_configuration import PURPLE
from app.configurations.files_configurations import BULLET_ICON_NAME


class ShootingWarriorInfo(BaseWarriorInfo):
    def __init__(self, warrior):
        super().__init__(warrior)
        self.add_category('bullets', str(len(self.warrior.bullets)), PURPLE, BULLET_ICON_NAME)

    def form_and_set_warrior_info(self):
        super().form_and_set_warrior_info()
        self.info['bullets'][1].update_text(len(self.warrior.bullets))
