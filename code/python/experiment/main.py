from environment import *
from gridworld import *
from agent import *
from models import *
from game import *

import os
from collections import defaultdict
import csv
import sys
import argparse
import numpy as np
import random



def parse_arguments():
    parser = argparse.ArgumentParser("simulated_agents argument parser")
    
    parser.add_argument('--generate-trials', action='store_true', help='generate experiment trials')
    parser.add_argument('--trial', type=int, default=0, help = 'which trial to generate specifically')
    parser.add_argument('--cf', action='store_true', default=False, help='run counterfactual model predictions')
    parser.add_argument('--hyp', action='store_true', default=False, help='run hypothetical model predictions')
    parser.add_argument('--visualize', action='store_true', default=False, help='run pygame animations and make gif')
    parser.add_argument('--verbose', action='store_true', default=False, help='verbosely print info while simulating or not')
    parser.add_argument('--save-trial-data', action='store_true', default=False, help='save trial data while generating trials')
    
    parser.add_argument('--n-simulations', type=int, default=1000, help='number of simulations to run counterfactual/hypothetical models')
    
    # Gridworld parameters
    parser.add_argument('--prob-stall', type=float, default=0.12, help='probabilty of agent stalling on any time step')
    parser.add_argument('--prob-door', type=float, default=0.19, help='probability of door switching on any time step')
    parser.add_argument('--time-limit', type=int, default=10, help='time limit for agent')

    return parser.parse_args()


def fix_seed(seed):
    np.random.seed(seed)
    random.seed(seed)


if __name__ == '__main__':
    arglist = parse_arguments()

    if arglist.make_image:
        if arglist.trial == 0:
            print('please specify a valid trial number with --trial')
            import sys; sys.exit(0)

        gw = GridWorld(prob_door = arglist.prob_door, time_limit = 1)
        gw.read_world(filename = arglist.trial)
        g = Game(gw, agent = None)
        g.on_init(no_sidebar = True)
        g.on_render()
        g.screenshot('grid_images/{}.png'.format(arglist.trial))
        g.on_cleanup()

    elif arglist.generate_trials:
        trials = read_trials()
        trial_data = []

        for trial in trials:
            trial_num = trial['num']
            fix_seed(trial_num)
            if arglist.trial > 0 and arglist.trial != trial_num:
                continue

            print('\n----- generating trial {} -----\n'.format(trial_num))
            gw = GridWorld(arglist.prob_door)
            gw.read_world(filename = str(trial_num))
            this_trial_data = {'trial': trial_num}
            trial_dir = 'trials/' + str(trial_num)

            a = Agent(path = trial['path'], prob_stall = arglist.prob_stall)

            # Run agent baseline and record outcome
            env = Environment(gw, a, generating_trials = True, trial_dir = trial_dir)
            original_runtime, outcome = env.run(door_changes = trial['door_changes'],
                verbose = arglist.verbose, visualize = arglist.visualize)
            this_trial_data['outcome'] = outcome

            # Run counterfactual model and record success rate
            if arglist.cf:
                cf = CounterfactualModel(env, 'counterfactual', original_runtime,
                                         door_changes = trial['door_changes'])
                rate = cf.simulate_all(num_simulations = arglist.n_simulations,
                                       verbose = arglist.verbose)
                this_trial_data['cf_success_rate'] = rate

            # Run hypothetical model and record success rate
            if arglist.hyp:
                hyp = HypotheticalModel(env, 'hypothetical')
                rate = hyp.simulate_all(num_simulations = arglist.n_simulations,
                                        verbose = arglist.verbose)
                this_trial_data['hyp_success_rate'] = rate
            
            trial_data.append(this_trial_data)

        # Save model predictions
        if arglist.save_trial_data:
            with open('../../experiment/experiment.csv', 'w') as outfile:
                w = csv.DictWriter(outfile, trial_data[0].keys())
                w.writeheader()
                w.writerows(trial_data)

