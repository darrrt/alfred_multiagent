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

controller = Controller(
        agentMode="arm",
        agentCount=2,
        visibilityDistance=1.5,
        scene="FloorPlan319",

        # step sizes
        # gridSize=self.gridSize,
        snapToGrid=True,
        rotateStepDegrees=90,

        # image modalities
        renderDepthImage=False,
        renderInstanceSegmentation=False,

        # camera properties
        # width=player_screen_width,
        # height=player_screen_height,
        # x_display=x_display,
        fieldOfView=90)

for scene_name in scene_dict.keys():
    task_config={}
    task_config["scene_name"]=scene_name
    task_config["objects"]={}
    # task_config["turk_annotations"]={}
    controller.reset(scene=scene_name)
    
    multiEvents = controller.step(action="GetReachablePositions")
    print(len(multiEvents.metadata["objects"]))
    for obj in multiEvents.metadata["objects"]:
        if not obj["name"] in task_config["objects"].keys():
            task_config["objects"][obj["name"]]=0    
        task_config["objects"][obj["name"]]+=1
    with open(os.path.join(root_path,'../../scene_info/{}.json'.format(scene_name)),'w') as f :
        f.write(json.dumps(task_config,sort_keys=False,indent=4,separators=(',',':')))
    