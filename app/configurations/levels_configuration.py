from configurations.files_configurations import BACKGROUND_NAME, GROUND_GRASS_BLOCK_NAME, \
    PINK_GROUND_BLOCK_NAME, WOODEN_BOX_BLOCK_NAME, WALL_BLOCK_NAME, \
    POWER_ICON_NAME, SHIELD_ICON_NAME, APPLE_ICON_NAME

SCHEMA_LETTER_TO_IMAGE = {
    '.': BACKGROUND_NAME,
    'G': GROUND_GRASS_BLOCK_NAME,
    'P': PINK_GROUND_BLOCK_NAME,
    'U': WOODEN_BOX_BLOCK_NAME,
    'W': WALL_BLOCK_NAME,
    'S': POWER_ICON_NAME,
    'T': SHIELD_ICON_NAME,
    'A': APPLE_ICON_NAME
}

SCHEMA_LETTER_TO_TYPE = {
    '.': 'background',
    'G': 'block',
    'P': 'block',
    'U': 'block',
    'W': 'block',
    'T': 'icon',
    'S': 'icon',
    'A': 'icon'
}