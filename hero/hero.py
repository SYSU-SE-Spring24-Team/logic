__all__ = ["HERO"]

from moving_range import *


class HERO:
    '''
    作战单位类
    '''

    ## 默认属性，形成对象后可以视作属性直接使用，如 object.name
    default_params = {
        ## 单位静态属性
        "name": "玩家名称六字",
        "max_hp": 50,
        "defence": 5,
        "attack": 20,
        "hit_rate": 0.7,
        "miss_rate": 0.1,
        "crit": 1.5,
        "crit_rate": 0.5,
        ## 单位动态属性
        #property "alive": True,
        "now_hp": 50,
        ## 场地静态属性
        "move_range": MOVING_RANGE(RANGE_TYPE.Manhatten, 1),
        "attack_range": MOVING_RANGE(RANGE_TYPE.Manhatten, 1),
        ## 场地动态属性
        #property "x": 0,
        #property "y": 0,
        "position": (0, 0),
    }

    def __init__(self, params: dict = {}, **kwargs) -> None:
        '''
        初始化属性
        params:dict,需要设置的属性
        **kwargs:dict,需要设置的属性
        如object = HERO(params, name="玩家名称")
        设置属性时优先级为kwargs>params>default_params
        未对注入攻击属性进行检查，需要自行检查
        '''
        self.__dict__.update(HERO.default_params)
        self.set(params, **kwargs)

    def set(self, params: dict = {}, **kwargs) -> None:
        '''
        设置属性
        params:dict,需要设置的属性
        **kwargs:dict,需要设置的属性
        使用方式同初始化
        设置属性时优先级为kwargs>params>now_params
        未对注入攻击属性进行检查，需要自行检查
        '''
        self.__dict__.update(params)
        self.__dict__.update(kwargs)

    def describe(self, param_keys: list = []) -> dict:
        '''
        描述属性
        param_keys:list，需要描述的属性，默认为空表示返回所有属性
        返回描述的属性
        '''
        return {
            key: self.__dict__[key]
            for key in param_keys
        } if param_keys else self.__dict__

    @property
    def alive(self) -> bool:
        '''
        是否存活，使用object.alive进行调用
        '''
        return self.now_hp > 0

    @property
    def x(self) -> int:
        '''
        x坐标，使用object.x进行调用
        为只读属性，设置x坐标请使用object.position = (x,y)
        '''
        return self.position[0]
    
    @property
    def y(self) -> int:
        '''
        y坐标，使用object.y进行调用
        为只读属性，设置y坐标请使用object.position = (x,y)
        '''
        return self.position[1]

    def __str__(self) -> str:
        return self.name


if __name__ == "__main__":
    '''
    测试
    '''
    params = {"name": "玩家名称", "max_hp": 200}
    ## 优先级为kwargs>params>default_params
    hero_list = [HERO(params, name=str(i)) for i in range(10)]
    for hero in hero_list:
        print(hero.describe(["name", "max_hp", "now_hp", "attack"]))

    ## 优先级为kwargs>params>now_params
    params_list = [{"name": "玩家名称", "max_hp": i * 100} for i in range(7)]
    for hero, params in zip(hero_list, params_list):
        hero.set(params, now_hp=5)

    print("==" * 20)
    for hero in hero_list:
        print(hero.describe(["name", "max_hp"]), "now_hp:",hero.now_hp, "'attack':",
              hero.attack)
