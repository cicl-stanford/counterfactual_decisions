from utils import *
import networkx as nx


class Rep:
    FLOOR = ' '      # empty square
    START_RED = 'r'
    START_BLUE = 'b'
    GOAL = 'g'
    DOOR = '|' 
    BLOCKED = 'X'    # blocked inaccessible square


rep_to_name = {
    Rep.FLOOR: 'Floor',
    Rep.START_RED: 'Start',
    Rep.START_BLUE: 'Start',
    Rep.GOAL: 'Goal',
    Rep.DOOR: 'Door',
    Rep.BLOCKED: 'Blocked'
}


# ------------------------------
class GridElement:
    def __init__(self, rep, location):
        self.rep = rep
        self.name = rep_to_name[rep]
        self.location = location
        if rep == Rep.START_RED:
            self.color = Color.LIGHT_RED
        elif rep == Rep.START_BLUE:
            self.color = Color.LIGHT_BLUE

    def __str__(self):
        return '{} at {}'.format(self.name, self.location)


class Door(GridElement):
    def __init__(self, door_properties, rep, location):
        GridElement.__init__(self, rep, location)
        self.prob = door_properties['prob']
        self.is_open = door_properties['is_open']
        self.is_open_original = door_properties['is_open']

    def __str__(self):
        state = 'open' if self.is_open else 'closed'
        return '{} {} at {}'.format(state, self.name, self.location)



# ------------------------------
class GridWorld():
    def __init__(self, prob_door, time_limit = 10):
        self.width = 0
        self.height = 0
        self.time_limit = time_limit
        self.prob_door = prob_door
        self.objects = []


    def read_world(self, filename):
        x = 0
        y = 0
        with open('grids/{}.txt'.format(filename), 'r') as file:
            phase = 1
            doors = []
            door_count = 0
            for line in file:
                line = line.strip('\n')
                if line == '':
                    phase += 1

                # PHASE 1: Read in and store door properties
                elif phase == 1:
                    l = line.split(' ')
                    doors.append({'prob': self.prob_door,
                                  'is_open': (int(l[0]) == 1)})
                
                # PHASE 2: Read in actual grid world setup
                elif phase == 2:
                    for x, rep in enumerate(line):
                        if rep == '.':
                            continue
                        if rep == '|':
                            newobj = Door(doors[door_count], rep, (x//2 + 1, y))
                            door_count += 1
                        elif rep in rep_to_name:
                            newobj = GridElement(rep, (x//2, y))
                        self.objects.append(newobj)
                    y += 1

        self.width = x//2 + 1
        self.height = y


    def print(self):
        for o in self.objects:
            print(o)


    def get_gridsquare_at(self, location):
        gridsquares = list(filter(lambda o: o.location == location and not\
            isinstance(o, Door), self.objects))
        not_floors = list(filter(lambda o: o.name != 'Floor', gridsquares))
        if len(not_floors) > 0:
            return not_floors[0]
        if len(gridsquares) > 0:
            return gridsquares[0]
        return None


    def get_door_right_of(self, location):
        if location[0] < self.width:
            location_right = self.get_new_location(location, RIGHT) 
            d = list(filter(lambda d: d.location == location_right,
                            self.get_doors()))
            if len(d) > 0: return d[0]
        return None
        

    def inbounds(self, location):
        x, y = location
        return min(max(x, 0), self.width - 1), min(max(y, 0), self.height - 1)

    
    def get_all_locations(self):
        return [(x, y) for x in range(self.width) for y in range(self.height)]


    def get_new_location(self, location, action):
        return self.inbounds([sum(x) for x in zip(location, action)])

    
    def get_start_location(self, color):
        starts = list(filter(lambda o: o.name == 'Start' and\
            o.color == str_to_color(color), self.objects))
        if len(starts) > 0: return starts[0].location
        return (0, 0)
            

    def get_goal_location(self):
        goals = list(filter(lambda o: o.name == 'Goal', self.objects))
        if len(goals) > 0: return goals[0].location
        return None


    def get_doors(self):
        return list(filter(lambda o: isinstance(o, Door), self.objects))

    
    def is_valid_action(self, location, action):
        # does not account for closed doors
        new_location = self.get_new_location(location, action)
        if action != STAY and location == new_location:
            return False
        
        new_gridsquare = self.get_gridsquare_at(new_location)
        if new_gridsquare.name == 'Blocked':
            return False
        
        return True


    def make_reachability_graph(self):
        self.reachability_graph = nx.Graph()
        for location in self.get_all_locations():
            self.reachability_graph.add_node(location)
            actions = [DOWN, UP, LEFT, RIGHT]
            for action in actions:
                if self.is_valid_action(location, action):
                    new_location = self.get_new_location(location, action)
                    if new_location in self.reachability_graph:
                        self.reachability_graph.add_edge(location, new_location)


    def get_gridsquares_between(self, location_one, location_two):
        self.make_reachability_graph()
        try:
            return nx.shortest_path_length(self.reachability_graph, location_one, location_two)
        except nx.NetworkXNoPath:
            pass
            
    def get_shortest_path(self, location_one, location_two):
        self.make_reachability_graph()
        try:
            return nx.shortest_path(self.reachability_graph, location_one, location_two)
        except nx.NetworkXNoPath:
            pass
