import pygame

from configurations.files_configurations import *
from configurations.modes_configuration import LEFT, RIGHT
from configurations.size_configurations import PART_OF_MAP_HEIGHT, PART_OF_MAP_WIDTH, HEIGHT, WARRIOR_SIZE

from services_for_game.music import Music
from services_for_game.camera import Camera
from .service_funcs import *

from abc import ABC, abstractmethod


class BaseWarrior(ABC, pygame.sprite.Sprite):
    def __init__(self, warrior_name: str, camera: Camera, init_side: str = 'right'):
        super(BaseWarrior, self).__init__()

        self.warrior_name = warrior_name
        self.camera = camera
        self.game = None
        self.music = Music()

        # Загружаем информацию из json файлов о персонаже, а также анимации различных состояний
        load_features_data(self)
        set_mode_to_images_dict(self)
        set_mode_to_frame_number_dict(self)

        self._set_conditions()

        # Задаём координаты и активное изображение
        self.image: pygame.Surface = self.mode_to_images[init_side]['idle'][0]
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x, self.rect.y = PART_OF_MAP_WIDTH, HEIGHT - self.rect.height - PART_OF_MAP_HEIGHT
        self.last_side = init_side

    def _set_conditions(self) -> None:
        """Задаёт условия состояний. В зависимости от этой конфигурации будет зависеть работа методов"""

        self.conditions = {
            'attack': {
                'status': False,
                'func': self._attack,
            },
            'jump': {
                'jumping_count': self.JUMPING_COUNT,
                'status': False,
                'func': self._jump,
                'just_finished': False,
            },
            'hurt': {
                'status': False,
                'func': None
            },
            'die': {
                'status': False,
                'func': None
            },
            'walk': {
                'directions': set(),
                'func': self._walk,
                'status': False
            },
            'run': {
                'directions': set(),
                'func': self._run,
                'status': False
            },
            'idle': {
                'func': self._idle,
                'status': True
            },
            'fall': {
                'func': self._fall,
                'status': False,
                'falling_speed': self.FALLING_ACCELERATION
            },
            'collect': {
                'func': self._collect,
                'status': False
            }
        }

    def _walk(self) -> None:
        """Метод вызывается при ходьбе"""
        if self.check_for_mode_presence('run'):  # Если мы бежим, то мы не идём
            return

        self._change_pos_while_walking()
        if self._cancel_transporting():  # Проверка на столкновение
            self._change_pos_while_walking(-1)

    def _change_pos_while_walking(self, reverse=1) -> None:
        """Изменяем позицию во время ходьбы. Если параметр reverse = -1,
        то отменяет последнее действие
        :param reverse: Индикатор отмены последнего действия
        """

        if self.last_side == LEFT:
            self.rect.x -= self.WALKING_SPEED * reverse
        if self.last_side == RIGHT:
            self.rect.x += self.WALKING_SPEED * reverse

    def _run(self) -> None:
        """Метод вызывается при беге"""

        if not self.check_for_mode_presence('walk'):   # Если мы не идём, то мы не можем бежать
            return

        self._change_pos_while_running()
        if self._cancel_transporting():  # Проверка на столкновение
            self._change_pos_while_running(-1)

    def _change_pos_while_running(self, reverse=1):
        """Изменяем позицию во время бега. Если параметр reverse = -1,
        то отменяет последнее действие
        :param reverse: Индикатор отмены последнего действия
        """

        if self.last_side == LEFT:
            self.rect.x -= self.RUNNING_SPEED * reverse
        if self.last_side == RIGHT:
            self.rect.x += self.RUNNING_SPEED * reverse

    def _fall(self) -> None:
        """Метод, вызывающийся при падении"""

        self._change_pos_while_falling()  # Изменяем координаты

        res = self._cancel_transporting()  # Проверка на столкновение
        if res:
            # Отменяем предыдущие изменения
            self._change_pos_while_falling(res)
            # Уменьшаем здоровье от падения и деактивируем состояние
            self.reduce_health_from_falling(self.conditions['fall']['falling_speed'])
            self.deactivate('fall', features_dict={'falling_speed': self.FALLING_ACCELERATION})

    def _change_pos_while_falling(self, collided_group: pygame.sprite.Group = None) -> None:
        """Обновляет позицию во время прыжка. В случае передачи группы спрайтов
        отменяет последнее действие"""

        if collided_group:
            self.rect.y = collided_group[0].rect.y - self.rect.height
        else:
            self.rect.y += self.conditions['fall']['falling_speed']
            self.conditions['fall']['falling_speed'] += self.FALLING_ACCELERATION

    def _jump(self) -> None:
        """Метод вызывается во время прыжка.
        В случае, если мы падаем вниз, то мы не можем прыгать.
        В случае, если мы заканчиваем прыжок, то мы деактивируем соответствующее состояние"""

        if self.check_for_mode_presence('fall'):  # Проверка на падение
            self.deactivate('jump')
            return

        self._change_pos_while_jumping()  # Изменение координат

        # Если у нас конец прыжка
        if self.conditions['jump']['jumping_count'] <= -(self.JUMPING_COUNT + 1):
            self.deactivate('jump', features_dict={'jumping_count': self.JUMPING_COUNT,
                                                   'just_finished': True})
            return

        res = self._cancel_transporting()  # Проверка на столкновение
        if res:
            self._change_pos_while_jumping(res)

    def _change_pos_while_jumping(self, collided_sprites: pygame.sprite.Group = None) -> None:
        """Изменяет позицию персонажа во время прыжка. В случае, если передается
        параметр collided_sprites, то последнее действие наоборот отменяется"""

        if collided_sprites:  # Если есть задетые спрайты, то отменяем действие
            if collided_sprites[0].rect.y < self.rect.y:
                # Если мы врезались головой (сверху нас препятствие)
                self.rect.y = collided_sprites[0].rect.y + collided_sprites[0].rect.height
                self.conditions['jump']['jumping_count'] = -1
            else:
                # Если вы врезались ногами (снизу нас препятствие)
                self.deactivate('jump', features_dict={'jumping_count': self.JUMPING_COUNT,
                                                       'just_finished': True})
                self.rect.y = collided_sprites[0].rect.y - self.rect.height
        else:  # Если задетых спрайтов нет, то просто обновляем координаты
            jumping_count = self.conditions['jump']['jumping_count']
            sign = 1 if jumping_count >= 0 else -1
            self.rect.y -= round((jumping_count ** 2) * self.JUMPING_K) * sign
            self.conditions['jump']['jumping_count'] -= 1
            print(self.rect.y, jumping_count)

    @abstractmethod
    def _attack(self) -> None:
        """Метод вызывается при атаке персонажа. Нуждается в переопределении в дочерних классах"""

        pass

    def _idle(self) -> None:
        """Метод вызывается при "ничего не делании" персонажа"""

        pass

    def _collect(self) -> None:
        """Метод активируется при сборе предметов. В случае, если рядом находится предмет, то
        вызывается его функия, а затем он уничтожается"""

        res = self._near_with_items()
        if res:
            res[0].func(self)
            res[0].kill()
            self.music.play_collecting_sound()
        self.deactivate('collect')

    def reduce_health_from_falling(self, falling_speed: int) -> None:
        """Уменьшает здоровье после падения
        :param falling_speed: Скорость падения
        :type falling_speed: int
        :return: None
        """

        if falling_speed <= 70:
            return
        self.health -= (falling_speed - 70) // 2
        self.music.play_hurting_sound()

    def activate(self, mode: str, direction: str = None) -> None:
        """Активирует состояние. В случае передачи направления
        также добавляет его в список направлений

        :param mode: Состояние
        :type mode: str
        :param direction: Направление
        :type direction: str
        """

        self.conditions[mode]['status'] = True
        if direction:
            self.last_side = direction
            self.conditions[mode]['directions'].add(direction)

    def _cancel_transporting(self) -> pygame.sprite.Group:
        """Возвращает список задетых блоков
        :return Список спрайтов
        :rtype pygame.sprite.Group
        """

        return pygame.sprite.spritecollide(self, self.game.map_blocks_group, False)

    def _near_with_items(self) -> pygame.sprite.Group:
        """Возвращает список задетых предметов
        :return Список спрайтов
        :rtype pygame.sprite.Group
        """

        return pygame.sprite.spritecollide(self, self.game.map_icons_group, False)

    def change_last_side(self, pos) -> None:
        """Меняет сторону, в которую будет смотреть персонаж в зависимости от направления атаки
        :param pos: Позиция клика мышки
        :return: None
        """

        delta_x, delta_y = self.camera.get_delta()  # Получаем сдвиг камеры для правильной обработки координат
        self.last_side = LEFT if pos[0] - delta_x <= self.rect.x + self.rect.width / 2 else RIGHT

    def deactivate(self, mode: str, direction: str = None, features_dict: dict = {}) -> None:
        """Принимаем на вход состояние, которое надо отключить.
        В случае, если также передается параметр direction,
        то из списка направления данного состояния удаляется это направление,
        а после этого возможны две ситуации. Если после удаления направления,
        список активных направлений пуст, то мы отключаем состояние.
        В противном случае - состояние не отключается.
        Также, можно передать словарь, ключи и значения которого
        будут установлены в настройках отключаемого состояния

        :param mode: Состояние
        :param direction: Направление
        :param features_dict: Дополнительные параметры

        :return None
        """

        if direction:  # Если указано направление, то удаляем его из списка
            self.conditions[mode]['directions'].discard(direction)
            if not self.conditions[mode]['directions']:
                self.conditions[mode]['status'] = False
            else:
                # Выбираем единственное оставшееся направление
                self.last_side = list(self.conditions[mode]['directions'])[0]
        else:
            self.conditions[mode]['status'] = False

        # Задаём значения состоянию
        for a, b in features_dict.items():
            self.conditions[mode][a] = b

    def update(self) -> None:
        """Обновляет позицию персонажа исходя из активных состояний"""

        modes = []  # Здесь будет список активных состояний
        for mode in self.conditions.keys():
            if self.conditions[mode]['status']:
                self.conditions[mode]['func']()  # Если состояние активно, то оно действует
                modes.append(mode)

        self.check_for_falling()  # Проверка на то, что мы падаем
        self.conditions['jump']['just_finished'] = False  # Индикация того,
        # что мы не только что закончили прыгать. Важно, так как от этого зависит будем ли мы падать

        # Выбираем режим, для которого будет рисоваться картинка и обновляем её
        mode = sorted(modes, key=lambda x: MODE_IMPORTANCE[x], reverse=True)[0]
        self._update_image(mode)

        # Настраиваем камеру
        self.camera.update(self)

    def check_for_mode_presence(self, *modes) -> bool:
        """Проверяем наличие состояний"""

        return all(self.conditions[mode]['status'] for mode in modes)

    def check_for_falling(self) -> None:
        """Проверяем то, что мы падаем. В случае падения активирует соответствующее состояние"""

        self.rect.y += 1
        # Если мы не прыгаем и не стоим на земле (касаемся блоков), то мы падаем
        if not (pygame.sprite.spritecollide(self, self.game.map_blocks_group, False)
                or self.conditions['jump']['status']):
            # Если мы только закончили прыгать, то скорость падения равна скорости падения в прыжке
            if self.conditions['jump']['just_finished']:
                self.conditions['fall']['falling_speed'] = round(self.JUMPING_COUNT ** 2 * self.JUMPING_K)
            self.activate('fall')
        self.rect.y -= 1

    def _update_image(self, mode: str) -> None:
        """Обновляет картинку по заданному состоянию
        :param mode: Состояние
        :type mode: str

        :return None
        :rtype: None
        """

        if mode == 'fall':  # Картинка для падения и прыжка одна и та же
            mode = 'jump'

        # Увеличиваем номер картинки в анимации и обновляем изображение
        self.mode_to_frame_number[self.last_side][mode] = (self.mode_to_frame_number[self.last_side][mode] + 1) % 7
        self.image = self.mode_to_images[self.last_side][mode][self.mode_to_frame_number[self.last_side][mode]]

    def __str__(self) -> str:
        result = [f'<Warrior> {self.warrior_name}', f'Здоровье: {self.health}, Урон: {self.power}',
                  f'Позиция: {self.rect.x, self.rect.y}']
        return '\n'.join(result)
