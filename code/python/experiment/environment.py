from game import *
from utils import get_action_from_location

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
from collections import defaultdict
from datetime import datetime



class Environment:
    def __init__(self, gridworld, agent, generating_trials = False,
                 trial_dir = 'trials'):
        self.world = gridworld
        self.agent = agent
        self.generating_trials = generating_trials
        self.trial_dir = trial_dir
        if not self.generating_trials:
            self.trial_dir += '/{}_{}'.format(self.world.name,
                    datetime.now().strftime('%m-%d-%y_%H-%M-%S'))
        self.agent.location = self.world.get_start_location(self.agent.path)
    

    def reached_goal(self):
        """ Checks if agent has reached goal """
        return self.world.get_goal_location() == self.agent.location


    def plan_path(self):
        """ Returns a sequence of actions to the goal from the agent's current location """
        goal_location = self.world.get_goal_location()
        path = []
        locations_in_path = self.world.get_shortest_path(self.agent.location, goal_location)
        for i in range(1, len(locations_in_path)):
            path.append(get_action_from_location(locations_in_path[i-1],
                                                 locations_in_path[i]))
        return path


    def execute(self, path, verbose):
        """ Executes a single action from given path, accounting for walls and doors """

        # Execute with uncertainty (random stalling)
        if not self.generating_trials and bernoulli(self.agent.prob_stall):
            if verbose: print('\tagent stalled')
            return
    
        action = tuple(path.pop(0))
        possible_door = self.world.get_door_right_of(self.agent.location)
        if (not self.world.is_valid_action(self.agent.location, action)) or (possible_door is not None and not possible_door.is_open):
            path.insert(0, action)
        else:
            new_location = self.world.get_new_location(self.agent.location, action)
            self.agent.move_to(new_location)
       

    def run(self, path = [], door_changes = defaultdict(lambda : []),
            original_runtime = 0, verbose = False, visualize = False,
            include_00 = True, no_sidebar = False):
        """ Simulates agent interacting with environment after planning path """
        
        # Initialize game visualization
        if visualize:
            self.game = Game(self.world, self.agent)
            self.game.on_init(no_sidebar = no_sidebar)
            
            make_dir(self.trial_dir)

            if not no_sidebar:
                # Visualize initial slide before decision 
                self.game.on_render(time = self.world.time_limit, chose = False)
                self.game.screenshot('{}/00.png'.format(self.trial_dir))
                
            # Visualize first slide with decision
            self.game.on_render(time = self.world.time_limit)
            self.game.screenshot('{}/01.png'.format(self.trial_dir))

        # Initialize planner if path empty, otherwise follow path
        self.outcome = 'lost'
        timestep = 0

        for timestep in range(1, self.world.time_limit + 1):
            if verbose: print('   timestep {}'.format(timestep))
            
            # Have planner generate initial path
            if len(path) == 0:
                path = self.plan_path()

            self.execute(path, verbose)
            if verbose: self.agent.print_status()
            
            # Probabilistically change doors
            for d in self.world.get_doors():
                if self.generating_trials or timestep <= original_runtime:
                    change_door = (str(timestep) in door_changes and\
                                  list(d.location) in door_changes[str(timestep)])
                elif bernoulli(d.prob):
                    change_door = True
                else:
                    change_door = False
                        
                if change_door:
                    d.is_open = not d.is_open
                    if verbose: print('\tdoor at {} changed'.format(d.location))

            if visualize:
                self.game.on_render(time = (self.world.time_limit - timestep))
                self.game.screenshot('{}/{:02d}.png'.format(self.trial_dir, timestep + 1))
            
            if self.reached_goal():
                self.outcome = 'won'
                if verbose: print('\treached goal!')
                break

        if visualize:
            self.finish_game(timestep, no_sidebar, include_00)

        return timestep, self.outcome


    def finish_game(self, timestep, no_sidebar, include_00):
        """ Visualizes last slide and generates gif of the whole trial """
        if not no_sidebar:
            self.game.on_render(time = (self.world.time_limit - timestep),
                                outcome = self.outcome)
            self.game.screenshot('{}/{:02d}.png'.format(self.trial_dir, timestep + 2))
        make_gif(self.trial_dir, self.trial_dir + '/full', include_00)
        self.game.on_cleanup()
        
    
    def reset(self):
        """ Resets state of all doors in the gridworld and location of the agent """
        
        for d in self.world.get_doors():
            d.is_open = d.is_open_original
        self.agent.location = self.world.get_start_location(self.agent.path)
        self.agent.reached_goal = False
        
