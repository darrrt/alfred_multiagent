import json 
import numpy as np 
import os,sys 
import re 

from ai2thor.controller import Controller


root_path=os.path.join(os.path.dirname(__file__),"./data/json_2.1.0/")
root_path_len=len(root_path)
# with open(os.path.join(root_path,'../../scene_dict.json'),'w') as f :
#     f.write(json.dumps(scene_dict,sort_keys=False,indent=4,separators=(',',':')))
with open(os.path.join(root_path,'../../scene_dict.json'),'r') as f :
    scene_dict=json.load(f)
gridSize=0.25
init_pos_max_robots=10
init_pos_random_times=50
controller = Controller(
        agentMode="arm",
        agentCount=2,
        visibilityDistance=1.5,
        scene="FloorPlan319",
        gridSize=gridSize,
        # step sizes
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
    task_config["gridSize"]=gridSize
    # task_config["RaablePositions"]={}
    # task_config["turk_annotations"]={}
    controller.reset(scene=scene_name)
    
    multiEvents = controller.step(action="GetRaablePositions")

    corners = np.array(multiEvents.metadata["sceneBounds"]['cornerPoints'])
    scene_most_left, scene_most_right, scene_most_top, scene_most_bottom = np.min(
        corners[:, 0]), np.max(corners[:, 0]), np.max(
            corners[:, 2]), np.min(corners[:, 2])
        
    x_len = int(np.floor((scene_most_right-scene_most_left) / gridSize +
                        1))
    y_len = int(np.floor((scene_most_top-scene_most_bottom) / gridSize +
                        1))
    
    gridBoard = np.zeros((x_len, y_len))

    raable_positions = multiEvents.metadata["actionReturn"]
    region = []
    for pos in raable_positions:
        x, y = pos['x'], pos['z']
        region.append([x, y])  
    
    task_config["RaablePositions"]=region
    region_np=np.array(region).reshape((-1,2))
    region_range=len(region)
    task_config["random"]={}
    for idx in range(init_pos_random_times):
        for robot in range(init_pos_max_robots):
            select_idxs=np.random.choice(region_range,init_pos_max_robots,replace=False)
            task_config["random"]["{}".format(idx)]=region_np[select_idxs,:].tolist()


    with open(os.path.join(root_path,'../../scene_info/{}_{}.json'.format(scene_name,gridSize)),'w') as f :
        f.write(json.dumps(task_config,sort_keys=False,indent=4,separators=(',',':')))
    # exit()
    
    