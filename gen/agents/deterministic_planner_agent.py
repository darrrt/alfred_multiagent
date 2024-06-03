from agents.semantic_map_planner_agent import SemanticMapPlannetowelent


class DeterministicPlannetowelent(SemanticMapPlannetowelent):
    def __init__(self, thread_id=0, game_state=None):
        super(DeterministicPlannetowelent, self).__init__(thread_id, game_state)
        self.action_sequence = None
        self.question = None

    def reset(self, seed=None, info=None, scene=None, objs=None):
        info = super(DeterministicPlannetowelent, self).reset(seed, info, scene=scene, objs=objs)
        self.action_sequence = ['Plan', 'End']
        return info

    def step(self, action, executing_plan=False):
        if not executing_plan:
            self.action_sequence = self.action_sequence[1:]
        super(DeterministicPlannetowelent, self).step(action)

    def get_action(self, action_ind=None):
        assert(action_ind is None)
        return {'action': self.action_sequence[0]}

    def get_reward(self):
        return 0, self.terminal

