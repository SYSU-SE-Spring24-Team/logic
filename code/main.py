from map import MAP
from hero import HERO
params={}
params["name"]="龙王"
params["now_sp"]=50
params["atk_range"]=1
params["atk_range_type"]=1
params["move_range"]=3
params["move_range_type"]=1
heros = HERO(params,8,8,1)
map=MAP()
map.add_object(heros)
params["name"]="狗王"
params["now_sp"]=30
params["atk_range"]=0
# params["move_range"]=3
heroes = HERO(params,9,9,2)
map.add_object(heroes)
map.run()
