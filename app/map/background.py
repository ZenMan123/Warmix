from app.configurations.levels_configuration import SCHEMA_LETTER_TO_IMAGE
from app.configurations.files_configurations import PATH_TO_BACKGROUNDS
from app.configurations.size_configurations import PART_OF_MAP_SIZE
from .map_part import MapPart


class Background(MapPart):
    def __init__(self, x, y, level, symbol=None):
        super(Background, self).__init__(x, y, level, symbol)
        self.path_to_image = f'{PATH_TO_BACKGROUNDS}/{SCHEMA_LETTER_TO_IMAGE[self.symbol]}'
        self.size = PART_OF_MAP_SIZE
        self.set_size_and_image(self.size, self.path_to_image)

