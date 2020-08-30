import pygame

from app.game.game import Game

from app.configurations.size_configurations import PART_OF_MAP_HEIGHT, PART_OF_MAP_WIDTH, HEIGHT, ANIMATIONS_COUNT
from app.configurations.modes_configuration import LEFT, RIGHT, MODE_IMPORTANCE

from app.services_for_game.music import Music
from app.services_for_game.camera import Camera

from app.map.tombstone import TombStone
from .abstract_warrior import AbstractWarrior
from abc import ABC, abstractmethod

from ..screen_drawers.base_warrior_info import BaseWarriorInfo


class BaseWarrior(AbstractWarrior, ABC):
    def __init__(self, login: str, warrior_name: str, camera: Camera, game: Game, music: Music):
        super(AbstractWarrior, self).__init__(login, warrior_name, game)
        super(ABC, self).__init__()

        self.camera = camera
        self.music = music

        self._set_conditions()  # Задаём словарь состояний и их параметры
        self.info = BaseWarriorInfo(self)

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
                'func': self._hurt,
                'hurting_count': -1
            },
            'die': {
                'status': False,
                'func': self._die,
                'dying_count': -1
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

    def _walk(self) -> bool:
        """Метод вызывается при ходьбе"""
        if self.check_for_mode_presence('run'):  # Если мы бежим, то мы не идём
            return False

        self._change_pos_while_walking()
        if self._cancel_transporting():  # Проверка на столкновение
            self._change_pos_while_walking(-1)
            return False
        return True

    def _change_pos_while_walking(self, reverse=1) -> None:
        """Изменяем позицию во время ходьбы. Если параметр reverse = -1,
        то отменяет последнее действие
        :param reverse: Индикатор отмены последнего действия
        """

        if self.last_side == LEFT:
            self.rect.x -= self.WALKING_SPEED * reverse
        if self.last_side == RIGHT:
            self.rect.x += self.WALKING_SPEED * reverse

    def _run(self) -> bool:
        """Метод вызывается при беге"""

        if not self.check_for_mode_presence('walk'):  # Если мы не идём, то мы не можем бежать
            return False

        self._change_pos_while_running()
        if self._cancel_transporting():  # Проверка на столкновение
            self._change_pos_while_running(-1)
            return False
        return True

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
            return False
        return True

    def _change_pos_while_falling(self, collided_group: pygame.sprite.Group = None) -> None:
        """Обновляет позицию во время прыжка. В случае передачи группы спрайтов
        отменяет последнее действие"""

        if collided_group:
            self.rect.y = collided_group[0].rect.y - self.rect.height
        else:
            self.rect.y += self.conditions['fall']['falling_speed']
            self.conditions['fall']['falling_speed'] += self.FALLING_ACCELERATION

    def _jump(self) -> bool:
        """Метод вызывается во время прыжка.
        В случае, если мы падаем вниз, то мы не можем прыгать.
        В случае, если мы заканчиваем прыжок, то мы деактивируем соответствующее состояние"""

        if self.check_for_mode_presence('fall'):  # Проверка на падение
            self.deactivate('jump')
            return False

        self._change_pos_while_jumping()  # Изменение координат

        # Если у нас конец прыжка
        if self.conditions['jump']['jumping_count'] <= -(self.JUMPING_COUNT + 1):
            self.deactivate('jump', features_dict={'jumping_count': self.JUMPING_COUNT,
                                                   'just_finished': True})
            return False

        res = self._cancel_transporting()  # Проверка на столкновение
        if res:
            self._change_pos_while_jumping(res)
            return False
        return True

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

    @abstractmethod
    def _attack(self) -> None:
        """Метод вызывается при атаке персонажа. Нуждается в переопределении в дочерних классах"""
        pass

    def _idle(self) -> None:
        """Метод вызывается при "ничего не делании" персонажа"""
        return

    def _die(self) -> bool:
        """Метод вызывается, когда здоровье персонажа становится неположительным.
        Если состояние die активировано, то никакие другие состояния не будут действовать.
        После исполнения анимации смерти, изображения героя сменится на значок могилы,
        а сам герой будет уничтожен"""

        if self.conditions['die']['dying_count'] == ANIMATIONS_COUNT - 1:
            self.kill()
            TombStone(self.rect, self.game)  # Создаём на нашем месте могилу
        else:
            self.conditions['die']['dying_count'] += 1
        return True

    def _hurt(self) -> bool:
        """Метод вызывается когда игрок теряет здоровье от АТАКИ (не от падения),
        так как это будет выглядеть не очень"""

        if self.conditions['hurt']['hurting_count'] == ANIMATIONS_COUNT - 1:
            self.deactivate('hurt', features_dict={'hurting_count': -1})
            return False
        else:
            self.conditions['hurt']['hurting_count'] += 1
            return True

    def _collect(self) -> None:
        """Метод активируется при сборе предметов. В случае, если рядом находится предмет, то
        вызывается его функия и проигрывается мелодия, а затем он уничтожается"""

        res = self._near_with_items()
        if res:
            res[0].func(self)
            res[0].sound()
            res[0].kill()
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
        """Обновляет позицию персонажа исходя из активных состояний.
        В случае, если мы умираем, никакое состояние не исполняется"""

        self.check_for_dying()  # Проверка на то, что мы умираем
        modes = []  # Здесь будет список активных состояний

        if self.check_for_mode_presence('die'):  # В случае смерти выполняется только одно состояние
            self.conditions['die']['func']()
            modes.append('die')
        else:
            for mode in self.conditions.keys():
                if self.conditions[mode]['status']:
                    if self.conditions[mode]['func']():  # Если состояние активно, то оно действует
                        modes.append(mode)

            self.check_for_falling()  # Проверка на то, что мы падаем
            self.conditions['jump']['just_finished'] = False  # Индикация того,
            # что мы не только что закончили прыгать. Важно, так как от этого зависит будем ли мы падать

        # Выбираем режим, для которого будет рисоваться картинка и обновляем её
        self._update_image(sorted(modes, key=lambda x: MODE_IMPORTANCE[x])[-1])

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

    def check_for_dying(self) -> None:
        if self.health <= 0:
            self.activate('die')

    def receive_damage(self, damage):
        self.activate('hurt')
        self.health -= damage