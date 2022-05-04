from gridworld import *
from utils import Color

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
import numpy as np
import random
from datetime import datetime


save_dir = 'trials'

_image_library = {}
def get_image(filename):
    global _image_library
    path = '../graphics/{}.png'.format(filename)
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path)
        _image_library[path] = image
    return image


class Game:
    def __init__(self, gridworld, agent = None):
        self._running = True
        self.world = gridworld
        self.agent = agent
        
        self.small_fsize = 18
        self.large_fsize = 42
        self.text_vspacing = 10

        self.scale = 80   # number of pixels per tile
        self.tile_size = (self.scale, self.scale)
        self.agent_r = 25
        self.agent_start_center = (self.scale//2, self.scale*3//2)
        self.eye_size = (16, 22)
        self.eye_offsets = [(-16, -18), (1, -18)]
        self.star_width = 60
        self.star_offset = ((self.scale - self.star_width)//2,
                            (self.scale - self.star_width)//2)
        self.sidebar_left = self.scale
        self.sidebar_right = self.scale * 2
        self.wall_width = 7  # odd so it can be centered
        self.door_width = 19
        self.door_jut = self.scale//6
        self.width = self.scale * self.world.width + self.wall_width
        self.screen_width = self.width + self.sidebar_left + self.sidebar_right
        self.height = self.scale * self.world.height + self.wall_width


    def on_init(self, no_sidebar = False):
        pygame.init()
        self.no_sidebar = no_sidebar
        if self.no_sidebar:
            self.screen = pygame.display.set_mode((self.width, self.height))
        else:
            self.screen = pygame.display.set_mode((self.screen_width, self.height))
            self.small_font = pygame.font.SysFont('Arial', self.small_fsize)
            self.large_font = pygame.font.SysFont('Arial', self.large_fsize)
        self._running = True


    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            # press enter to save
            if event.key == pygame.K_RETURN:
                image_name = '{}_{}.png'.format(self.world.name,
                             datetime.now().strftime('%m-%d-%y_%H-%M-%S'))
                self.screenshot('{}/{}'.format(save_dir, image_name))
                return
            if event.key in KeyToTuple.keys():
                action = KeyToTuple[event.key]
                self.agent.location = inbounds(np.add(self.agent.location, action),
                        self.world.width, self.world.height)


    def on_render(self, chose = True, time = 0, outcome = ''):
        self.draw_gridsquares()
        self.draw_agent(chose)
        if not self.no_sidebar:
            self.draw_timer(time)
            self.draw_outcome(outcome)
        pygame.display.flip()
        pygame.display.update()


    def draw_gridsquares(self):
        self.screen.fill(Color.WHITE)

        for location in self.world.get_all_locations():
            if location == (0, 1): continue
            tl = self.top_left(location)
            fill = pygame.Rect(tl[0], tl[1], self.scale, self.scale)
            self.screen.fill(Color.FLOOR, fill)
            pygame.draw.rect(self.screen, Color.LINE, fill, 1)
            
        for o in self.world.objects:
            tl = self.top_left(o.location)
            fill = pygame.Rect(tl[0], tl[1], self.scale, self.scale)
            if o.name == 'Start':
                self.screen.fill(o.color, fill)
            if o.name == 'Blocked':
                self.screen.fill(Color.BLACK, fill)
            elif o.name == 'Goal':
                star = pygame.transform.scale(get_image('goal'),
                        (self.star_width, self.star_width))
                self.screen.blit(star, np.add(tl, self.star_offset))
            elif isinstance(o, Door):
                if o.is_open:
                    self.draw_door(start = tl, diff = (0, self.door_jut))
                    self.draw_door(start = (tl[0], tl[1] + self.scale),
                        diff = (0, -self.door_jut))
                else:
                    self.draw_door(start = tl, diff = (0, self.scale))

        self.draw_perimeter()

    
    def draw_door(self, start, diff):
        pygame.draw.line(self.screen, Color.DOOR, start_pos = start,
            end_pos = np.add(start, diff), width = self.door_width)


    def draw_wall(self, start, diff):
        pygame.draw.line(self.screen, Color.WALL, start_pos = start,
            end_pos = np.add(start, diff), width = self.wall_width)
    

    def draw_agent(self, chose):
        if self.agent is None:
            return
        if not chose:
            center = self.agent_start_center
        else:
            center = np.add(self.top_left(self.agent.location),
                            (self.scale//2, self.scale//2))
        pygame.draw.circle(self.screen, Color.AGENT, center, self.agent_r)
        pygame.draw.circle(self.screen, Color.WHITE, center, self.agent_r, 2)
        eye = pygame.transform.scale(get_image('eye'), self.eye_size)
        self.screen.blit(eye, np.add(center, self.eye_offsets[0]))   # left eye
        self.screen.blit(eye, np.add(center, self.eye_offsets[1]))   # right eye

    
    def draw_timer(self, time):
        text_surface = self.small_font.render('time left:', True, Color.BLACK)
        text_w, text_h = text_surface.get_size()
        text_w_margin = (self.sidebar_right - text_w)//2
        self.screen.blit(text_surface, (self.width + self.sidebar_left +\
            text_w_margin, self.text_vspacing * 4))
        
        surface = self.large_font.render(str(time), True, Color.BLACK)
        w, h = surface.get_size()
        w_margin = (self.sidebar_right - w)//2
        self.screen.blit(surface, (self.width + self.sidebar_left + w_margin,
                                   self.text_vspacing * 5 + text_h))

    
    def draw_outcome(self, outcome):
        text_surface = self.small_font.render('result:', True, Color.BLACK)
        text_w, text_h = text_surface.get_size()
        text_w_margin = (self.sidebar_right - text_w)//2
        self.screen.blit(text_surface, (self.width + self.sidebar_left +\
            text_w_margin, self.height//2 + self.text_vspacing * 3))
        if outcome != '':
            surface = self.large_font.render(outcome.upper(), True, Color.BLACK)
            w, h = surface.get_size()
            w_margin = (self.sidebar_right - w)//2
            self.screen.blit(surface, (self.width + self.sidebar_left + w_margin,
                                       self.height//2 + self.text_vspacing * 4 + text_h))
        

    def draw_perimeter(self):
        self.draw_wall(self.top_left((0, 0)), (self.scale * self.world.width, 0))
        self.draw_wall(self.top_left((self.world.width, 0)),
                       (0, self.scale * self.world.height))
        self.draw_wall(self.top_left((0, self.world.height)),
                       (self.scale * self.world.width, 0))
        self.draw_wall(self.top_left((0, 1)),
                       (self.scale * (self.world.width - 1), 0))
        self.draw_wall(self.top_left((self.world.width - 1, 1)),
                       (0, self.scale))
        self.draw_wall(self.top_left((0, 2)),
                       (self.scale * (self.world.width - 1), 0))


    def screenshot(self, image_path):
        pygame.image.save(self.screen, image_path)


    def top_left(self, loc):
        tl = (self.scale * loc[0] + self.wall_width//2,
              self.scale * loc[1] + self.wall_width//2)
        return tl if self.no_sidebar else np.add(tl, (self.sidebar_left, 0))

    
    def on_cleanup(self):
        pygame.display.quit()
        pygame.quit()


    def on_execute(self, no_sidebar = False):
        if self.on_init(no_sidebar) == False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_render()
        self.on_cleanup()

