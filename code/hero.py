class HERO(object):
    def __init__(self,params,x=0,y=0,faction=0):
        # params用于返回属性参数信息
        if params.get("name") == None:
            self.name="玩家名称六字"#玩家名称
        else:
            self.name=params["name"]

        if params.get("max_hp") == None:
            self.max_hp=100       #最大血量
        else:
            self.max_hp=params["max_hp"]
        
        if params.get("now_hp") == None:
            self.now_hp=100       #当前血量
        else:
            self.now_hp=params["now_hp"]
        
        if params.get("sheild") == None:
            self.sheild=100       #护盾量
        else:
            self.sheild=params["sheild"]
        
        if params.get("defen") == None:
            self.defen=10           #防御力
        else:
            self.defen=params["defen"]
        
        if params.get("atk") == None:
            self.atk=100           #攻击力
        else:
            self.atk=params["atk"]
        
        if params.get("crit") == None:
            self.crit=0         #暴击概率
        else:
            self.crit=params["crit"]
        
        if params.get("crit_rate") == None:
            self.crit_rate=1.5    #暴击倍率
        else:
            self.crit_rate=params["crit_rate"]

        if params.get("vampirism") == None:
            self.vampirism=0       #吸血率
        else:
            self.vampirism=params["vampirism"]
        
        if params.get("miss_rate") == None:
            self.miss_rate=0    #闪避率
        else:
            self.miss_rate=params["miss_rate"]
        
        if params.get("hit_rate") == None:
            self.hit_rate=1.0     #命中率
        else:
            self.hit_rate=params["hit_rate"]
        
        if params.get("true_damage") == None:
            self.true_damage=0    #额外真实伤害
        else:
            self.true_damage=params["true_damage"]
        
        if params.get("move_sp") == None:
            self.move_sp=30       #移动消耗的sp
        else:
            self.move_sp=params["move_sp"]
        
        if params.get("atk_sp") == None:
            self.atk_sp=50        #攻击消耗的sp
        else:
            self.atk_sp=params["atk_sp"]
        
        if params.get("now_sp") == None:
            self.now_sp=0         #当前的sp(为0就可以开始行动)
        else:
            self.now_sp=params["now_sp"]
        
        if params.get("atk_range") == None:
            self.atk_range=1         #攻击距离
        else:
            self.atk_range=params["atk_range"]
        
        if params.get("atk_range_type") == None:
            self.atk_range_type=1         #攻击距离类型(1是曼哈顿距离,2是切比雪夫距离)
        else:
            self.atk_range_type=params["atk_range_type"]
        
        if params.get("move_range") == None:
            self.move_range=1         #移动距离
        else:
            self.move_range=params["move_range"]
        
        if params.get("move_range_type") == None:
            self.move_range_type=1         #移动距离类型(1是曼哈顿距离,2是切比雪夫距离)
        else:
            self.move_range_type=params["move_range_type"]



        #格挡、反击、反伤有空再加
        self.x=x    #在地图上的位置
        self.y=y
        self.faction=faction  #势力(目前1是我方、2是敌方、小于等于0的是一些障碍)


