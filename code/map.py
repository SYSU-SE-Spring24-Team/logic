from hero import HERO
import random
class MAP(object):
    def __init__(self,n=10,m=10):
        self.n=n   #地图范围为[0,self.n) * [0,self.m)
        self.m=m
        self.tim=0
        self.object=[]
    
    def add_object(self,a):
        self.object.append(a)

    def clean(self,x):  #清除x这个人
        for i in range(0,len(self.object)):
            if x is self.object[i]:
                del self.object[i]
                break
    
    def win(self):      #判断游戏是否已经结束
        human1=0
        human2=0
        for human in self.object:
            if human.faction == 1:
                human1+=1
            elif human.faction == 2:
                human2+=1
        if human1 == 0:
            return 2    #势力2赢了
        elif human2 == 0:
            return 1    #势力1赢了
        return 0
    
    def wt(self):       
        minn=1e100
        for human in self.object:
            if human.faction == 1 or human.faction == 2:
                minn = min(minn,human.now_sp)
        cnt = 0
        self.tim += minn
        
        for human in self.object:
            if human.faction == 1 or human.faction == 2:
                human.now_sp-=minn
                if human.now_sp == 0:
                    cnt += 1
        return cnt

    def get_priority(self,target,x,y):
        if target.x==x and target.y==y:
            return 0
        for human in self.object:
            if human.x==x and human.y==y:
                if human.faction == target.faction:
                    return -1
                else:
                    return 1
        return 0
    def ai(self,x):
        pri = -1e100    # 优先级越大越好
        xx = 0 
        yy = 0 
        typ = 0         # type=1则攻击,type=2则移动
        tmp = None
        target = self.object[x]
        opt1 = target.faction % 2
        for human in self.object:
            opt2 = human.faction % 2
            if opt1 ^ opt2 == 1:
                if target.atk_range_type == 1:
                    if abs(target.x-human.x)+abs(target.y-human.y)<=target.atk_range:
                        pp = self.get_priority(target,human.x,human.y)
                        if pp>pri:
                            pri = pp
                            xx = human.x
                            yy = human.y
                            typ = 1
                            tmp = human

                elif target.atk_range_type == 2:
                    if max(abs(target.x-human.x),abs(target.y-human.y))<=target.atk_range:
                        pp = self.get_priority(target,human.x,human.y)
                        if pp>pri:
                            pri = pp
                            xx = human.x
                            yy = human.y
                            typ = 1
                            tmp = human
        
        lt=[[0 for i in range(self.m)]for j in range(self.n)]
       
        for human in self.object:
            lt[human.x][human.y]=1
        
        for i in range(0,self.n):
            for j in range(0,self.m):
                if lt[i][j]==1:
                    continue
                if target.move_range_type == 1:
                    if abs(target.x-i)+abs(target.y-j)<=target.move_range:
                        pp = self.get_priority(target,i,j)
                        if pp>pri:
                            pri = pp
                            xx = i
                            yy = j
                            typ = 2
                elif target.move_range_type == 2:
                    if max(abs(target.x-i),abs(target.y-j))<=target.move_range:
                        pp = self.get_priority(target,i,j)
                        if pp>pri:
                            pri = pp
                            xx = i
                            yy = j
                            typ = 2
        if typ == 0:
            self.rest(target)
        elif typ == 1:
            self.attack(target,tmp)
        elif typ == 2:
            self.move(target,xx,yy)

    def message_atk(self,target,tmp,hel,type):
        #此时需要向前端传递消息
        if type == 1:
            print("{0}对{1}造成了{2}的伤害".format(target.name,tmp.name,hel))
        elif type == 2:
            print("{0}闪避了!".format(tmp.name))
        elif type == 4:
            print("{0}打出了暴击!".format(target.name))
        elif type == 5:
            print("{0}通过吸血回复了{1}的血量".format(target.name,hel))
        elif type == 6:
            print("{0}对{1}的护盾造成了{2}的伤害!".format(target.name,tmp.name,hel))
        elif type == 7:
            print("{0}倒下了!".format(tmp.name))

    def attack(self,target,tmp):
        if target.atk_range_type == 1 or target.atk_range_type == 2:
            k = (target.atk*target.atk)/(target.atk+tmp.defen)
            k = int(k)
            ki = target.hit_rate-tmp.miss_rate
            e = random.random()
            if e>=ki:
                self.message_atk(target,tmp,0,2)
            e = random.random()
            ki = target.crit
            if e<=ki:
                self.message_atk(target,tmp,0,4)
            k = max(1,k)
            if tmp.sheild!=0:
                if tmp.sheild>=k:
                    tmp.sheild-=k
                    self.message_atk(target,tmp,k,6)
                    k=0
                else:
                    self.message_atk(target,tmp,tmp.sheild,6)
                    k-=tmp.sheild
                    tmp.sheild=0
            k += target.true_damage
            if k != 0: 
                self.message_atk(target,tmp,k,1)
            tmp.now_hp -= k
            if target.vampirism!=0 and k!=0:
                target.now_hp += k*target.vampirism
                self.message_atk(target,tmp,tmp.k*target.vampirism,5)
            target.now_hp=min(target.now_hp,target.max_hp)
        target.now_sp+=target.atk_sp
        if tmp.now_hp<0:
            self.message_atk(target,tmp,0,7)
            self.clean(tmp)
        

    def move(self,target,x,y):
        print("{0}从({1},{2})移动到了({3},{4})".format(target.name,target.x,target.y,x,y))
        target.x=x
        target.y=y
        target.now_sp+=target.move_sp
        #此处需要发送消息给前端
        pass

    def rest(self,target):
        print("{0}选择休息".format(target.name))
        target.now_sp+=min(target.atk_sp,target.move_sp)
    
    

    def run(self):
        faction = 0
        j = 0
        while self.win() == 0:
            cnt = self.wt()
            tmp = random.randint(1,cnt)
            j = 0
            for human in self.object:
                if human.faction == 1 or human.faction == 2:
                    if human.now_sp == 0:
                        tmp -= 1
                if tmp == 0:
                    faction = human.faction
                    break
                j += 1
            if faction == 1:
                # self.ai(j)
                #此处需要让self.object的第i个变量行动
                pass
            elif faction == 2:
                self.ai(j)  #让ai行动
        

