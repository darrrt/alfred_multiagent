import json 
import numpy as np 
import os,sys 
import re 
import time 

from ai2thor.controller import Controller
from NL2HLTLtaskPlanner import utils as util

root_path="/home/user/xsj/LLMTaskPlanning/alfred_multiagent/data/json_2.1.0/"
root_path_modified="/home/user/xsj/LLMTaskPlanning/alfred_multiagent/task_wo_position/"
root_path_len=len(root_path)
# with open(os.path.join(root_path,'../../scene_dict.json'),'w') as f :
#     f.write(json.dumps(scene_dict,sort_keys=False,indent=4,separators=(',',':')))
with open(os.path.join(root_path,'../../scene_dict.json'),'r') as f :
    scene_dict=json.load(f)

max_tasks_per_env=5
max_tasks_composed=10
np.random.seed(42)

GPTinterface=util.GPTinterface(
            useFakeGPTAPI=(not True),
            readFromFormerLog=False,
            logger=None,
            TranslateNL2TLInterface=util.NL2TLTranslater(
                    machine_type='openaiAPI',
                    base_url = "127.0.0.1:8000"
                # communicatorWithServer=util.communicator.communicationViaSSH(
                #     connectCommand="mill19",
                #     serverFolderPath='/home/icl-mill19/xsj/model_weight/scp-folder',
                #     clientFolderPath='/home/icl-mill19/xsj/NL2HLTL/exp',
                #     fileName='prompt.txt',)
                    ),
            )

count=0
for scene_name in scene_dict.keys():
    with open(os.path.join(root_path,'../../multiagent_longtasks/{}.json'.format(scene_name)),'r') as f :
        task_config=json.load(f)
    for n_task in range(2,max_tasks_composed):
        if "tasks_{}".format(n_task) in task_config.keys():
            task_lists=task_config["tasks_{}".format(n_task)]
            count+=len(task_lists)
print(count)
# exit()
for scene_name in scene_dict.keys():
    with open(os.path.join(root_path,'../../multiagent_longtasks/{}.json'.format(scene_name)),'r') as f :
        task_config=json.load(f)
    for n_task in range(2,max_tasks_composed):
        if "tasks_{}".format(n_task) in task_config.keys():
            task_lists=task_config["tasks_{}".format(n_task)]
            print(scene_name,'n_task',n_task,'len(task_lists)',len(task_lists))
            for tasks_id in range(len(task_lists)):
                if not "finetuned" in task_lists[tasks_id]["finetuned"]:
                    try:
                    # if True:
                        prompt=[
                        {"role": "system",
                        "content": """I have a set of primitive subtasks for robots. 
    Help me combine primitive subtasks into a larger task by randomly selecting several primitive subtasks. There can be temporal constraints between primitive subtasks. Below is the demonstrating example: 

    [Place two scoops in the top drawer to the left of the stove ; Put two measuring cups in a drawer on the kitchen island near the sink, ; Gather two ladles and store them in the cabinet to the right of the fridge.]

    output example 
    Place two scoops in the top drawer to the left of the stove at any time. Simultaneously, put two measuring cups in a drawer on the kitchen island near the sink.After placing the scoops, gather two ladles and store them in the cabinet to the right of the fridge.

    What I am particularly interested in is that, in one example, sibling task logical relationships can be, some subtasks need to be done sequentially; while some subtasks can be done in any order; some tasks can be done in any order; some task can only be done after some tasks happend and finished; task A cannot be done until task B finished; task A must be done before task B; subtasks should be done in sequence; task A should be done after task B; task can be done in any time."""
                        },{
                        "role": "user",
                        "content": """ Below is the new set of primitive subtasks:
    {}
    please generate 3 different composes
    please return in json:
    ```json
        {{
            "fintune 1": "",
            "fintune 2": ...,
            "fintune 3": ...,
        }}
    ```
    """.format(task_lists[tasks_id]["task_list"])
                        }
                        ]
                        # print(prompt)

                        ret=GPTinterface.communicate(prompt,task_stage='Q_envInfoExtraction',modelVersion='3',print_screen=False)
                        print(ret)
                        jsonstr=util.splitJSONfromTXT(ret)[-1]
                        
                        task_lists[tasks_id]["finetuned"]=json.loads(jsonstr)
                        
                        # with open(os.path.join(root_path,'../../multiagent_longtasks/{}.json'.format(scene_name)),'w') as f :
                        #     f.write(json.dumps(task_config,sort_keys=False,indent=4,separators=(',',':')))
                        # exit()
                        # check_flag=False
                    except:
                        pass

    with open(os.path.join(root_path,'../../multiagent_longtasks/{}.json'.format(scene_name)),'w') as f :
        f.write(json.dumps(task_config,sort_keys=False,indent=4,separators=(',',':')))
    print("rewrite",scene_name)

    
