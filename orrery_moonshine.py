#Orrery in hours
import math
import datetime

DAY = 1/24

WIDTH = 600
WC = WIDTH/2
HEIGHT = 600
HC = HEIGHT/2

SUN_RADIUS = 80
MERCURY_ORBIT = 100
MERCURY_RADIUS = 3

EARTH_ORBIT = 180
EARTH_RADIUS = 20
MOON_ORBIT = 40
MOON_RADIUS = 10

MOON_COLOUR  = (70, 70, 70)
MOON_SHINE_COLOUR = (220, 220, 255)
SUN_COLOUR   = (255, 255, 0)
EARTH_COLOUR = (0, 128, 196)
EARTH_ROT_COLOUR = (128, 255, 128)
MERCURY_COLOUR = (128, 128, 128)

EARTH_DAY = 1/24 * 2 * math.pi
MOON_ROTATION = EARTH_DAY * 1/27.322
EARTH_YEAR = EARTH_DAY * 1/364.25
MERCURY_YEAR = EARTH_DAY * 1/87.969


class Orrery:
    def __init__(self):
        self.hour = 0
        self.earth_coordinate = None
        self.earth_outer_line = None
        self.moon_coordinate = None
        self.moonshine_coordinate = None
        self.mercury_position = 0
        self.mercury_coordinate = None
        self.speed_factor = 2

    def set_earth_position(self):
        earth_x = math.cos(self.earth_position) * EARTH_ORBIT + WC
        earth_y = math.sin(self.earth_position) * EARTH_ORBIT + HC

        earth_rot_x = math.cos(self.earth_rotation) * EARTH_RADIUS + earth_x
        earth_rot_y = math.sin(self.earth_rotation) * EARTH_RADIUS + earth_y

        self.earth_coordinate = earth_x, earth_y
        self.earth_rot_coord = earth_rot_x, earth_rot_y

    def set_moon_position(self):
        earth_x, earth_y = self.earth_coordinate
        moon_x = math.cos(self.moon_position) * MOON_ORBIT + earth_x
        moon_y = math.sin(self.moon_position) * MOON_ORBIT + earth_y
        self.moon_coordinate = moon_x, moon_y

    def set_moonshine_position(self):
        # This is going to be pi (180) + earth_position.
        position = self.earth_position + math.pi
        moonshine_x = math.cos(position) * 3 + self.moon_coordinate[0]
        moonshine_y = math.sin(position) * 3 + self.moon_coordinate[1]
        self.moonshine_coordinate = moonshine_x, moonshine_y

    def set_mercury_position(self):
        mercury_x = math.cos(self.mercury_position) * MERCURY_ORBIT + WC
        mercury_y = math.sin(self.mercury_position) * MERCURY_ORBIT + HC
        self.mercury_coordinate = mercury_x, mercury_y

    def update(self, dt):
        self.hour += dt * self.speed_factor * 24
        self.earth_rotation = self.hour  * EARTH_DAY
        self.earth_position = self.hour * EARTH_YEAR
        self.moon_position = self.hour * MOON_ROTATION
        self.mercury_position = self.hour * MERCURY_YEAR
        self.set_earth_position()
        self.set_moon_position()
        self.set_moonshine_position()
        self.set_mercury_position()

    def get_time(self):
        return datetime.datetime.utcfromtimestamp(self.hour * 60 * 60).isoformat()

orrery = Orrery()

def update(dt):
    orrery.update(dt)

def on_key_down(key):
    if key == keys.EQUALS:
        orrery.speed_factor += 1
    elif key == keys.MINUS:
        orrery.speed_factor -= 1
    elif key == keys.K_0:
        orrery.speed_factor = 1


def draw():
    screen.fill((0, 0, 0))
    screen.draw.filled_circle((WC, HC), SUN_RADIUS, SUN_COLOUR)

    screen.draw.filled_circle(orrery.mercury_coordinate, MERCURY_RADIUS, MERCURY_COLOUR)

    screen.draw.filled_circle(orrery.earth_coordinate, EARTH_RADIUS, EARTH_COLOUR)
    screen.draw.line(orrery.earth_coordinate, orrery.earth_rot_coord, EARTH_ROT_COLOUR)

    screen.draw.filled_circle(orrery.moonshine_coordinate, MOON_RADIUS, MOON_SHINE_COLOUR)
    screen.draw.filled_circle(orrery.moon_coordinate, MOON_RADIUS, MOON_COLOUR)

    screen.draw.text(orrery.get_time(), (10, 10), color="white")
    screen.draw.text(str(orrery.hour), (10, 40), color="white")
    screen.draw.text(str(orrery.speed_factor), (300, 10), color="white")