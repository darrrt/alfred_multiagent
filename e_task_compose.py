import json 
import numpy as np 
import os,sys 
import re 

from ai2thor.controller import Controller


root_path="/home/user/xsj/LLMTaskPlanning/alfred_multiagent/data/json_2.1.0/"
root_path_modified="/home/user/xsj/LLMTaskPlanning/alfred_multiagent/task_wo_position/"
root_path_len=len(root_path)
# with open(os.path.join(root_path,'../../scene_dict.json'),'w') as f :
#     f.write(json.dumps(scene_dict,sort_keys=False,indent=4,separators=(',',':')))
with open(os.path.join(root_path,'../../scene_dict.json'),'r') as f :
    scene_dict=json.load(f)

def check_task(task_instruction):
    task_instruction=task_instruction.lower()
    if "two" in task_instruction:
        return False
    if "another" in task_instruction:
        return False
    return True

max_tasks_per_env=5
max_tasks_composed=10
np.random.seed(42)
for scene_name in scene_dict.keys():
    
    with open(os.path.join(root_path,'../../multiagent_longtasks/{}.json'.format(scene_name)),'r') as f :
        task_config=json.load(f)
    
    select_pool_names=np.sort(list(task_config["trials"].keys()))
    select_pool=np.arange(0,len(select_pool_names),step=1,dtype=np.int16)
    
    for n_task in range(1,min(max_tasks_composed,len(select_pool_names))):
        
        task_config["tasks_{}".format(n_task)]=[]
        for task_id in range(min(int(len(select_pool_names)/2),max_tasks_per_env)):
            print(scene_name,'n_task',n_task,'NO.',task_id)
            compose_check=False
            test_time=0
            while compose_check==False and test_time<100:
                compose_check=True
                test_time+=1
                ran_select=np.random.choice(select_pool,size=n_task,replace=False)
                used_objs=set()
                for idx in ran_select:
                    possible_obj=set(task_config["trials"][select_pool_names[idx]]["relative_objects"])
                    if len(possible_obj&used_objs)>0:
                        compose_check=False
                        break
                    else:
                        used_objs=used_objs|possible_obj
            if compose_check:
                task_config["tasks_{}".format(n_task)].append({
                    "task_list":[task_config["trials"][select_pool_names[idx]]["tasks"][0] for idx in ran_select],
                    "orign":[select_pool_names[ran_select].tolist()]
                })
    with open(os.path.join(root_path,'../../multiagent_longtasks/{}.json'.format(scene_name)),'w') as f :
        f.write(json.dumps(task_config,sort_keys=False,indent=4,separators=(',',':')))
    