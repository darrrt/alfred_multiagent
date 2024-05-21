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

for scene_name in scene_dict.keys():
    print('current',scene_name)
    task_config={}
    task_config["scene_name"]=scene_name
    task_config["trials"]={}
    # task_config["turk_annotations"]={}
    with open(os.path.join(root_path,"../../scene_info/{}.json".format(scene_name)),'r') as f:
        scene_config=json.load(f)
    possible_objects=trial_names= [re.match("([a-zA-Z]+)",x.lower()).group(0) for x in scene_config["objects"].keys()]
    
    for trial_path in scene_dict[scene_name]:
        if os.path.exists(os.path.join(root_path_modified,trial_path+'.json')):
            print('exists',os.path.join(root_path_modified,trial_path+'.json'))
            try:
                with open(os.path.join(root_path_modified,trial_path+'.json'),'r') as f:
                    relative_objects=json.load(f)["relative_objects"]
                can_handle=True
                for obj in relative_objects:
                    if not obj.lower() in possible_objects:
                        can_handle=False
            except:
                can_handle=False
            if can_handle:
                print(scene_name,'can handle',trial_path)
                with open(os.path.join(root_path,trial_path),'r') as f:
                    turk_annotations=json.load(f)["turk_annotations"]
                checked_tasks=[]
                for task in turk_annotations["anns"]:
                    if check_task(task["task_desc"]):
                        checked_tasks.append(task)
                if len(checked_tasks)>0:
                    task_config["trials"][trial_path]={}
                    task_config["trials"][trial_path]["tasks"]=checked_tasks
                    task_config["trials"][trial_path]["relative_objects"]=list(set(relative_objects))
            
    with open(os.path.join(root_path,'../../multiagent_longtasks/{}.json'.format(scene_name)),'w') as f :
        f.write(json.dumps(task_config,sort_keys=False,indent=4,separators=(',',':')))
    