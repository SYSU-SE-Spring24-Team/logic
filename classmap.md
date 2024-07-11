```mermaid
classDiagram
    direction LR
    class RANGE_TYPE {
        <<enumeration>>
        Manhattan 曼哈顿距离
        Chebyshev 切比雪夫距离
    }
    class MOVING_RANGE{
        RANGE_TYPE range_type 范围类型
        range_value 范围大小
        get_range(x,y,x_range,y_range) 返回能够到达的位置
    }
    MOVING_RANGE o-- RANGE_TYPE
    class HERO{
        name 名称
        max_hp 最大血量
        defence 防御值
        attack 攻击值
        hit_rate 命中率
        miss_rate 闪避率
        crit 暴击倍率
        crit_rate 暴击率
        --
        now_hp 当前血量
        -alive 存活状态
        --
        move_range 移动范围
        attack_range 攻击范围
        --
        position 位置
        -x 位置横坐标
        -y 位置纵坐标

        set() 批量设置属性
    }
    class EFFECT{
        <<interface>>
        -log 日志
        __init__(source,target) 效果
    }
    class ATTACK_EFFECT{
        -log 日志
        __init__(source,target) 攻击效果 攻击来源，攻击目标
    }
    class MOVE_EFFECT{
        -log 日志
        __init__(source,target) 移动效果 移动来源，移动目标位置
    }
    ATTACK_EFFECT <|-- EFFECT : 继承
    MOVE_EFFECT <|-- EFFECT : 继承
    HERO <-- ATTACK_EFFECT : 作用于
    HERO <-- MOVE_EFFECT : 作用于
```

## 攻击效果
```mermaid
flowchart LR
  attack(攻击力) --> hit{命中}
  hit -->|未命中| miss(伤害=0)
  hit -->|命中| crit{会心}
  crit -->|未暴击| damage1(伤害=攻击力-防御力)
  crit -->|暴击| damage2(伤害=攻击力*暴击率-防御力)
```

$$
\begin{align*}
damage = \begin{cases}
0 & p_{hit} > source.hit
\\
source.attack - target.defence & p_{hit} \leq source.hit_rate \land p_{crit} > source.crit_rate
\\
source.crit * source.attack - target.defence & p_{hit} \leq source.hit_rate \land p_{crit} \leq source.crit_rate
\end{cases}
\end{align*}
$$
