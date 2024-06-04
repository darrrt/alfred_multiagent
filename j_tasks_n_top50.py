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

task_configs={}
for n_task in range(1,max_tasks):
    # count tasks 
    task_descriptions_relevant_path=os.path.join(os.path.dirname(__file__),'multiagent_tasks_{}_summary_with_robot_init_pos.json'.format(n_task))
                                                 
    with open(task_descriptions_relevant_path,'r') as f:
        jsontxt=f.read()
        task_descriptions=json.loads(jsontxt)
        
    with open(os.path.join(os.path.dirname(__file__),'top_50_multiagent_tasks_{}_summary_with_robot_init_pos.json'.format(n_task)),'w') as f :
        f.write(json.dumps(task_descriptions[:50],sort_keys=False,indent=4,separators=(',',':')))