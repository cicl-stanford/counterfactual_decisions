from utils import opp_color

import copy


class Model:
    def __init__(self, env, model_type, original_runtime = 0, door_changes = {}):
        self.env = copy.deepcopy(env) # copy over agent and gridworld
        self.env.generating_trials = False
        self.model_type = model_type # counterfactual or hypothetical
        self.original_runtime = original_runtime
        self.door_changes = door_changes
   

    def simulate_once(self, verbose):
        self.env.reset()
        _, outcome = self.env.run(door_changes = self.door_changes,
                original_runtime = self.original_runtime, verbose = verbose)
        return outcome == 'won'


    def simulate_all(self, num_simulations, verbose = False):
        # Initialize cf/hyp agent to be the opposite
        self.env.agent.path = opp_color(self.env.agent.path)

        # Run simulations and track success rate
        num_successes = 0
        print('running {} model with {} path...'.format(self.model_type,
                self.env.agent.path))
        
        for i in range(num_simulations):
            if verbose:
                print('simulation', i+1)
            else:
                if i > 0 and i % 100 == 0: print(i, 'simulations done')
            num_successes += self.simulate_once(verbose)
            
        success_rate = int(num_successes / num_simulations * 100)
        print('{} success rate on {} path was {}% across {} simulations\n'.format(
               self.model_type, self.env.agent.path, success_rate, num_simulations))
            
        return success_rate



class CounterfactualModel(Model):
    def __init__(self, env, model_type, original_runtime, door_changes):
        Model.__init__(self, env, "counterfactual", original_runtime, door_changes)



class HypotheticalModel(Model):
    def __init__(self, env, model_type):
        Model.__init__(self, env, "hypothetical")

