PART_OF_MAP_SIZE = PART_OF_MAP_WIDTH, PART_OF_MAP_HEIGHT = 200, 200
AMOUNT_OF_PARTS_IN_ROW, AMOUNT_OF_PARTS_IN_COL = 20, 16

SIZE = WIDTH, HEIGHT = PART_OF_MAP_WIDTH * AMOUNT_OF_PARTS_IN_ROW, PART_OF_MAP_HEIGHT * AMOUNT_OF_PARTS_IN_COL
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1250, 680

WARRIOR_SIZE = WARRIOR_WIDTH, WARRIOR_HEIGHT = SCREEN_WIDTH // 10, SCREEN_HEIGHT // 5
BULLET_SIZE = BULLET_WIDTH, BULLET_HEIGHT = WARRIOR_WIDTH // 8, WARRIOR_HEIGHT // 8
RIP_SIZE = RIP_WIDTH, RIP_HEIGHT = WARRIOR_WIDTH, WARRIOR_HEIGHT
INFO_SIZE = INFO_WIDTH, INFO_HEIGHT = round(PART_OF_MAP_HEIGHT * 0.2), round(PART_OF_MAP_HEIGHT * 0.2)
ICON_SIZE = ICON_WIDTH, ICON_HEIGHT = round(PART_OF_MAP_HEIGHT * 0.3), round(PART_OF_MAP_HEIGHT * 0.3)

FPS = 30
ANIMATIONS_COUNT = 7