PATH_TO_BACKGROUNDS = 'static/textures/backgrounds/'
PATH_TO_BLOCKS = 'static/textures/blocks'
PATH_TO_ICONS = 'static/textures/icons'
PATH_TO_WEAPONS = 'static/warriors/weapons'
PATH_TO_WARRIOR = 'static/warriors'
PATH_TO_MUSIC = 'static/music'

BACKGROUND_NAME = 'background.png'
GROUND_GRASS_BLOCK_NAME = 'ground_grass.png'
PINK_GROUND_BLOCK_NAME = 'pink_ground.png'
WOODEN_BOX_BLOCK_NAME = 'wooden_box.png'
WALL_BLOCK_NAME = 'wall.png'

HEALTH_ICON_NAME = 'health.png'
POWER_ICON_NAME = 'power.png'
TIME_ICON_NAME = 'time.png'
POTION_ICON_NAME = 'potion.png'
SHIELD_ICON_NAME = 'shield.png'
APPLE_ICON_NAME = 'apple.png'
BULLET_ICON_NAME = 'bullet.png'
RIP_ICON_NAME = 'rip.png'

LEFT_BULLET_NAME = 'left_bullet.png'
RIGHT_BULLET_NAME = 'right_bullet.png'

MUSIC_BACKGROUND_NAME = 'background.mp3'
COLLECTING_SOUND_NAME = 'collecting.wav'
HURTING_SOUND_NAME = 'hurting.wav'
JUMPING_SOUND_NAME = 'jumping.wav'
ATTACKING_SOUND_NAME = 'attacking.wav'
BULLET_SHOOTING_NAME = 'bullet_shooting.wav'
EMPTY_MAGAZINE_NAME = 'empty_magazine.wav'
APPLE_EATING_NAME = 'apple_eating.wav'
COLLECTING_SWORD_NAME = 'collect_sword.wav'


def get_warrior_features_path(warrior_name: str) -> str:
    return f'{PATH_TO_WARRIOR}/{warrior_name}/features.json'


def get_warrior_photos_path(warrior_name: str, side: str, mode: str) -> str:
    return f'{PATH_TO_WARRIOR}/{warrior_name}/photos/{mode}/{side}'
