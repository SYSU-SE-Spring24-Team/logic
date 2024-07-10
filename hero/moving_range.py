__all__ = ['RANGE_TYPE', 'MOVING_RANGE']

from enum import Enum, auto


class RANGE_TYPE(Enum):
    '''
    移动范围类型
    '''

    ## 无视障碍：|x1-x2|+|y1-y2|<=range_value
    Manhatten = auto()
    ## 无视障碍：max(|x1-x2|,|y1-y2|)<=range_value
    Chebyshev = auto()


def range_distance(
    range_type: RANGE_TYPE,
    x_from: int,
    y_from: int,
    x_to: tuple[int, int] | int,
    y_to: tuple[int, int] | int,
    range_limit: int = 0,
) -> list[tuple[int, int, int]]:
    '''
    计算两点之间的距离
    type:RANGE_TYPE,移动范围类型
    x_from:int,起始x坐标
    y_from:int,起始y坐标
    x_to:tuple[int,int] | int,目标x坐标或目标x坐标范围
    y_to:tuple[int,int] | int,目标y坐标或目标y坐标范围
    range_limit:int，距离限制，默认为0，表示不限制
    返回列表，每个元素为(距离,x坐标,y坐标)
    '''
    from itertools import product
    if isinstance(x_to, int):
        x_to = (x_to, x_to + 1)
    if isinstance(y_to, int):
        y_to = (y_to, y_to + 1)

    xy_generator = product(range(*x_to), range(*y_to))
    if range_type == RANGE_TYPE.Manhatten:
        calc_distance = lambda x, y: abs(x_from - x) + abs(y_from - y)
    elif range_type == RANGE_TYPE.Chebyshev:
        calc_distance = lambda x, y: max(abs(x_from - x), abs(y_from - y))

    return [(dis, x, y) for x, y in xy_generator
            if (dis := calc_distance(x, y)) <= range_limit]


class MOVING_RANGE:
    '''
    移动范围类
    '''

    def __init__(self,
                 range_type: RANGE_TYPE = RANGE_TYPE.Manhatten,
                 range_value: int = 1) -> None:
        '''
        初始化移动范围
        range_type:RANGE_TYPE,移动范围类型
        range_value:int,移动范围值
        '''
        self.range_type = range_type
        self.range_value = range_value

    def get_range(
            self,
            x: int,
            y: int,
            x_range: tuple[int, int] | None = None,
            y_range: tuple[int, int] | None = None) -> list[tuple[int, int]]:
        '''
        获取移动范围
        x:int,当前x坐标
        y:int,当前y坐标
        x_range:tuple[int,int]，x坐标范围左闭右开，默认为None，表示不限制
        y_range:tuple[int,int]，y坐标范围左闭右开，默认为None，表示不限制
        返回移动范围
        '''
        if x_range is None:
            x_range = (x - self.range_value, x + self.range_value + 1)
        if y_range is None:
            y_range = (y - self.range_value, y + self.range_value + 1)

        return range_distance(self.range_type, x, y, x_range, y_range,
                              self.range_value)


if __name__ == "__main__":
    '''
    测试
    '''
    moving_range = MOVING_RANGE(RANGE_TYPE.Manhatten, 1)
    print(moving_range.get_range(0, 0))
    print(moving_range.get_range(0, 0, (-1, 1), (-1, 1)))
    print("=" * 20)
    moving_range = MOVING_RANGE(RANGE_TYPE.Chebyshev, 1)
    print(moving_range.get_range(0, 0))
    print(moving_range.get_range(0, 0, (-1, 1), (-1, 1)))
    print("=" * 20)
    moving_range = MOVING_RANGE(RANGE_TYPE.Manhatten, 2)
    print(moving_range.get_range(0, 0))
    print(moving_range.get_range(0, 0, (-1, 1), (-1, 1)))
    print("=" * 20)
    moving_range = MOVING_RANGE(RANGE_TYPE.Chebyshev, 2)
    print(moving_range.get_range(0, 0))
    print(moving_range.get_range(0, 0, (-1, 1), (-1, 1)))
    print("=" * 20)
