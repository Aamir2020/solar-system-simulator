
# Solar System Simulator
A two dimensional simulation of our solar system. Utilized n-body simulation and considered each object as a particle. This simulation doesn't include moons and asteroids. In addition, it doesn't take into account the rotation of planets or their roche limit.

The inital conditions for the planets are obtained from NASA's [horizon systems](https://ssd-api.jpl.nasa.gov/doc/horizons.html) API.

The current simulation utilizes a simple Euler integration to find numerical solution for the gravitational interactions.

## Installation

Use `pip` package manager to install the required packages:

```bash
python3 -m pip install -r requirements.txt
```

## The following celestial objects will be displayed
- Mercury
- Venus
- Earth
- Mars
- Jupiter
- Saturn
- Uranus
- Neptune
