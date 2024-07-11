__all__ = ["ATTACK_EFFECT", "MOVE_EFFECT"]

log_string = {
    "ATTACK": "{source}对{target}造成了{hit_hp}的伤害",
    "CRIT": "暴击！{source}对{target}造成了{hit_hp}的伤害",
    "MISS": "{source}尝试攻击，但是未命中{target}",
    "DIE": "{target}血量归零，死亡",
    "MOVE": "{source}从{source_position}移动到了{target}"
}

from abc import ABC, abstractmethod
from random import random

from hero import HERO

check_point = lambda s: random() < s


class EFFECT(ABC):
    '''
    效果基类
    '''

    def __init__(self,
                 source: HERO,
                 target: HERO | tuple[int, int] | None = None) -> None:
        '''
        初始化效果
        会在初始化时执行效果
        source:HERO,效果来源
        target:HERO|tuple[int,int]|None,效果目标
        '''
        self._log = []

        self.source = source
        self.target = target
        self._work()

    @abstractmethod
    def _work(self) -> None:
        '''
        执行效果
        '''
        pass

    def _add_log(self, log_type: str) -> None:
        '''
        添加日志，会自主使用log_string中的字符串，并使用self.__dict__进行格式化
        log_type:str,日志类型
        '''
        self._log.append(log_string[log_type].format(**self.__dict__))

    @property
    def log(self) -> list[str]:
        '''
        返回只读日志，使用object.log进行调用
        '''
        return self._log


class ATTACK_EFFECT(EFFECT):
    '''
    攻击效果，无距离检测
    source:HERO,攻击来源
    target:HERO,攻击目标
    '''

    def _work(self) -> None:
        ## 命中检查
        hit_check = check_point(
            self.source.hit_rate) and not check_point(self.target.miss_rate)
        ## 暴击检查
        crit_check = check_point(self.source.crit_rate)
        ## 计算命中伤害
        attack = self.source.attack
        if not hit_check:
            attack = 0
        elif crit_check:
            attack *= self.source.crit
        ## 结算伤害
        self.hit_hp = attack - self.target.defence
        if hit_check:
            if crit_check:
                self._add_log("CRIT")
            else:
                self._add_log("ATTACK")
            self.target.now_hp -= self.hit_hp
        else:
            self._add_log("MISS")
        ## 死亡检查
        if self.target.now_hp <= 0:
            self.target.now_hp = -1
            self._add_log("DIE")


class MOVE_EFFECT(EFFECT):
    '''
    移动效果，无距离检测
    source:HERO,移动来源
    target:tuple[int,int],移动目标坐标
    '''

    def _work(self) -> None:
        ## 移动效果
        self.source_position = self.source.position
        self.source.position = self.target
        self._add_log("MOVE")


if __name__ == "__main__":
    '''
    测试
    '''
    heros = [HERO(name="A", position=(1, 2)), HERO(name="B", position=(4, 3))]
    source = 0
    cnt = 10
    while all(hero.alive for hero in heros) and (cnt := cnt - 1) > 0:
        target = 1 - source

        # 会在初始化时执行效果
        attack_effect = ATTACK_EFFECT(heros[source], heros[target])
        print(attack_effect.log)

        # 会在初始化时执行效果
        move_effect = MOVE_EFFECT(source=heros[source],
                                  target=(heros[source].x - round(random()),
                                          heros[target].x + 1))
        print(move_effect.log)

        print(
            *[hero.describe(["name", "now_hp", "position"]) for hero in heros])
        print("=" * 20)
        source = target
