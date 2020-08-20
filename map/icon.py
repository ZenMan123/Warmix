from .map_part import MapPart
from configurations.size_configurations import PART_OF_MAP_WIDTH, PART_OF_MAP_HEIGHT, ICON_WIDTH, ICON_SIZE
from configurations.files_configurations import PATH_TO_ICONS
from configurations.levels_configuration import SCHEMA_LETTER_TO_IMAGE


class Icon(MapPart):
    def __init__(self, x, y, level, symbol):
        super(Icon, self).__init__(x, y, level, symbol)
        self.path = f'{PATH_TO_ICONS}/{SCHEMA_LETTER_TO_IMAGE[self.symbol]}'
        self.size = ICON_SIZE

        self.set_size_and_image(self.size, self.path)

        self.rect.x += (PART_OF_MAP_WIDTH - ICON_WIDTH) // 2
        self.rect.y += PART_OF_MAP_HEIGHT - self.rect.height - 5

        self.func = letter_to_func[self.symbol]


def get_func_with_set_value(func, value):
    def res_func(*args):
        func(*args, value=value)

    return res_func


def increase_health(obj, value):
    obj.health = min(obj.MAX_HEALTH * 2, obj.health + value)


def increase_power(obj, value):
    obj.power = min(obj.MAX_POWER * 2, obj.power + value)


letter_to_func = {
    'A': get_func_with_set_value(increase_health, 20),
    'T': get_func_with_set_value(increase_power, 5),
    'P': get_func_with_set_value(increase_power, 10),
    'S': get_func_with_set_value(increase_health, 30)
}
