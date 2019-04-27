#Orrery in hours
import math
import datetime

DAY = 1/24

WIDTH = 600
WC = WIDTH/2
HEIGHT = 600
HC = HEIGHT/2


class SolarObject:
    def __init__(self, anchor=None, orbital_velocity=0, rotational_velocity=0, radius=1, orbit=0, colour=(128, 128, 128),
        rotation_marker_colour=None):
        """Orbital and rotational velocities should be in radians per second."""
        self.anchor = anchor
        self.orbital_velocity = orbital_velocity
        self.rotational_velocity = rotational_velocity
        self.radius = radius
        self.orbit = orbit
        self.colour = colour
        self.position = 0, 0
        self.rotation = 0
        self.rotation_outer = 0, 0
        self.rotation_marker_colour = rotation_marker_colour

    def update(self, timestamp):
        """Timestamp should be in seconds floating since epoch"""
        cx, cy = self.anchor.position
        if self.orbit > 0:
            orbital_position = self.orbital_velocity * timestamp
            self.position = (math.cos(orbital_position) * self.orbit + cx,
                             math.sin(orbital_position) * self.orbit + cy)
        else:
            self.position = cx, cy
        if self.rotational_velocity:
            self.rotation = self.rotational_velocity * timestamp
            self.rotation_outer = (math.cos(self.rotation) * self.radius + self.position[0],
                                   math.sin(self.rotation) * self.radius + self.position[1])

    def draw(self):
        screen.draw.filled_circle(self.position, self.radius, self.colour)
        if self.rotational_velocity and self.rotation_marker_colour:
            screen.draw.line(self.position, self.rotation_outer, self.rotation_marker_colour)

class Orrery:
    def __init__(self):
        self.objects = []
        self.speed_factor = 2
        self.timestamp = 0

    def update(self, dt):
        self.timestamp += dt * self.speed_factor * 3600 * 24
        for item in self.objects:
            item.update(self.timestamp)

    def draw(self):
        for item in self.objects:
            item.draw()

    def get_time(self):
        return datetime.datetime.utcfromtimestamp(self.timestamp).isoformat()

    def add(self, item):
        self.objects.append(item)

EARTH_DAY = 1/24 * 2 * math.pi / 3600
MOON_ROTATION = EARTH_DAY * 1/27.322
EARTH_YEAR = EARTH_DAY * 1/364.25
MERCURY_YEAR = EARTH_DAY * 1/87.969
VENUS_YEAR = EARTH_DAY * 1/224.65

orrery = Orrery()
sun_anchor = SolarObject()
sun_anchor.position = WC, HC
sun = SolarObject(anchor=sun_anchor, radius=40, colour=(255, 255, 0))
orrery.add(sun)
# mercury
orrery.add(SolarObject(anchor=sun, radius=3, orbit=57, orbital_velocity=EARTH_DAY * 1/87.969))
# venus
orrery.add(SolarObject(anchor=sun, radius=6, orbit=108, orbital_velocity=EARTH_DAY * 1/224.65, colour=(255, 240, 180)))
earth = SolarObject(anchor=sun, radius=6, orbit=149, orbital_velocity=EARTH_DAY * 1/364.25, rotational_velocity=EARTH_DAY,
    colour=(0, 128, 196), rotation_marker_colour=(128, 255, 128))
orrery.add(earth)
moon = SolarObject(anchor=earth, radius=2, orbit=10, orbital_velocity=EARTH_DAY * 1/27.322, colour=(70, 70, 70))
orrery.add(moon)
mars = SolarObject(anchor=sun, radius=4, orbit=227, orbital_velocity=EARTH_DAY * 1/687, colour=(255, 90, 90))
orrery.add(mars)
phobos = SolarObject(anchor=mars, radius=1, orbit=6, orbital_velocity=EARTH_DAY * 3)
orrery.add(phobos)
deimos = SolarObject(anchor=mars, radius=1, orbit=23, orbital_velocity=EARTH_DAY * 24 / 30)
orrery.add(deimos)

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
    orrery.draw()

    screen.draw.text(orrery.get_time(), (10, 10), color="white")
    screen.draw.text(str(orrery.timestamp), (10, 40), color="white")
    screen.draw.text(str(orrery.speed_factor), (300, 10), color="white")