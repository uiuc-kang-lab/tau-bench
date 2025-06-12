from tau_bench.types import Action
import sys, json

traj_file = sys.argv[1]

required_task_actions = {
    12: [
        Action(name="get_reservation_details", kwargs={"reservation_id": "3FRNFB"})
    ],
    13: [
        Action(name="get_reservation_details", kwargs={"reservation_id": "XEWRD9"})
    ],
    15: [
        Action(name="get_reservation_details", kwargs={"reservation_id": "GV1N64"})
    ],
    17: [
        Action(name="get_reservation_details", kwargs={"reservation_id": "4NQLHD"})
    ],
    18: [
        Action(name="get_reservation_details", kwargs={"reservation_id": "SI5UKW"})
    ],
    21: [
        Action(name="get_reservation_details", kwargs={"reservation_id": "DF89BM"})
    ],
    24: [
        Action(name="get_reservation_details", kwargs={"reservation_id": "HXDUBJ"})
    ],
    35: [
        Action(name="get_reservation_details", kwargs={"reservation_id": "PEP4E0"})
    ],
    36: [
        Action(name="get_reservation_details", kwargs={"reservation_id": "PEP4E0"})
    ],
    37: [
        Action(name="get_user_details", kwargs={"user_id": "mei_brown_7075"})
    ],
    38: [
        Action(name="get_reservation_details", kwargs={"reservation_id": "H8Q05L"})
    ],
    39: [
        Action(name="get_reservation_details", kwargs={"reservation_id": "H8Q05L"})
    ],
    40: [
        Action(name="get_user_details", kwargs={"user_id": "sophia_silva_7557"})
    ],
    41: [
        Action(name="get_reservation_details", kwargs={"reservation_id": "3RK2T9"})
    ],
    42: [
        Action(name="get_reservation_details", kwargs={"reservation_id": "3RK2T9"})
    ],
    48: [
        Action(name="get_reservation_details", kwargs={"reservation_id": "EUJUY6"})
    ],
    49: [
        Action(name="get_reservation_details", kwargs={"reservation_id": "MDCLVA"})
    ]
}

with open(traj_file, "r") as f:
    traj = json.load(f)

original_rewards = []
regraded_rewards = []
for task_traj in traj:
    original_rewards.append(task_traj["reward"])
    if task_traj["task_id"] in required_task_actions:
        if task_traj["reward"] == 1:
            r_action = True
            for required_action in required_task_actions[task_traj["task_id"]]:
                found_action = False
                action_name = required_action.name
                action_kwargs = required_action.kwargs
                for action in task_traj["traj"]:
                    if "tool_calls" not in action or action["tool_calls"] is None:
                        continue
                    for tool_call in action["tool_calls"]:
                        if isinstance(tool_call["function"]["arguments"], str):
                            tool_call_function_arguments = json.loads(tool_call["function"]["arguments"])
                        else:
                            tool_call_function_arguments = tool_call["function"]["arguments"]
                        if tool_call_function_arguments == action_kwargs and tool_call["function"]["name"] == action_name:
                            found_action = True
                            break
                if not found_action:
                    r_action = False
                    break
            if r_action:
                regraded_rewards.append(1)
            else:
                regraded_rewards.append(0)
                # print(f"############ Task {task_traj['task_id']} failed to regrade ############")
                # print(f"agent traj:\n{json.dumps(task_traj['traj'], indent=2)}")
                # print(f"required actions: {required_task_actions[task_traj['task_id']]}")
        else:
            regraded_rewards.append(0)
    else:
        regraded_rewards.append(task_traj["reward"])

original_pass1 = sum(original_rewards) / len(original_rewards)
regraded_pass1 = sum(regraded_rewards) / len(regraded_rewards)
print(f"Original Pass@1: {original_pass1:.4f}")
print(f"Regraded Pass@1: {regraded_pass1:.4f}")
