
import pygame
from pygame import *

################################################
#
# This is a list of the different custom events used in the game
# when a character action (other than movement) is performed, one of these events
# will be posted and the pulled in the gameplay loop to dictate actions
#
################################################

# Event for testing
TEST_EVENT = pygame.event.Event(pygame.USEREVENT, attr='Event1')

# Event for when you kill an animal
KILL_ANIMAL = pygame.event.Event(pygame.USEREVENT, attr='KillAnimal')
