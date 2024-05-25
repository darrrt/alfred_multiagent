import json 
import numpy as np 
import os,sys 
import re 

from ai2thor.controller import Controller


root_path=os.path.join(os.path.dirname(__file__),"./data/json_2.1.0/")
root_path_len=len(root_path)

gridSize=0.25
init_pos_max_robots=10
init_pos_random_times=50
max_tasks=10
np.random.seed(42)
with open(os.path.join(root_path,'../../scene_dict.json'),'r') as f :
    scene_dict=json.load(f)
scene_init_config={}
for scene_name in scene_dict.keys():
    with open(os.path.join(root_path,'../../scene_info/{}_{}.json'.format(scene_name,gridSize)),'r') as f :
        scene_init_config[scene_name]=json.load(f)["random"]

with open(os.path.join(root_path,'../../multiagent_longtasks_summary.json'),'r') as f :
    task_config=json.load(f)
config_sort_w_tasks={}
for idx in range(max_tasks):
    config_sort_w_tasks[idx]=[]
for name in task_config.keys():
    for idx in range(max_tasks):
        if ".tasks_{}.".format(idx) in name:
            config_sort_w_tasks[idx].append(name)
            break

task_configs={}
for n_task in range(max_tasks):
    # count tasks 
    if not len(config_sort_w_tasks[n_task])>0:
        continue
    select=np.random.choice(len(config_sort_w_tasks[n_task]),len(config_sort_w_tasks[n_task]),replace=False)
    task_configs=[]
    for idx in select:
        scene_name=config_sort_w_tasks[n_task][idx].split('.')[0]
        init_pos=[]
        init_pos_select_list=np.random.choice(init_pos_random_times,5,replace=False).tolist()
        for n_pos in init_pos_select_list:
            init_pos.append(scene_init_config[scene_name]["{}".format(n_pos)])
        task_configs.append({
            config_sort_w_tasks[n_task][idx]:task_config[config_sort_w_tasks[n_task][idx]],
            "init_pos":init_pos,
            "init_pos_from":init_pos_select_list
        })
            
    with open(os.path.join(root_path,'../../multiagent_tasks_{}_summary_with_robot_init_pos.json'.format(n_task)),'w') as f :
        f.write(json.dumps(task_configs,sort_keys=False,indent=4,separators=(',',':')))