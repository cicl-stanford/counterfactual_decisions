class Agent:
    def __init__(self, path, prob_stall):
        self.path = path
        self.prob_stall = prob_stall
        self.location = (0, 0)
        
    def print_status(self):
        print("\tagent is currently at {}".format(self.location))
	
    def move_to(self, new_location):
        self.location = new_location
