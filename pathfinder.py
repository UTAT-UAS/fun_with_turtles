from simulator import Simulator, intersects  # intersects may be useful ;)


class YourSim(Simulator):
    def __init__(self):
        # Settings for the simulation
        Simulator.__init__(self)
        # Define your instance attributes here

    """
    self.area
    Is the box you must stay within the first element is
    the top left corner and the second is the bottom lefts.

    self.target is the target you are aiming to reach.
    self.boxes is a list of boxes that you must not pass through!
    They are in the same format as area

    self.left(theta) turn left theta degrees
    self.right(theta) turn right theta degrees
    self.forward() move forward 1 unit
    """
    def setup(self):
        pass

    def update(self):
        pass


if __name__ == '__main__':
    # Set up for the simulation PLZ have fun with
    sim = YourSim()
    dist_traveled = sim.simulate(0.001)
    if dist_traveled:
        print(f'You reached the target in {dist_traveled} steps')
    else:
        print("Failed to reach target became soup :_C")
    sim.exit()
