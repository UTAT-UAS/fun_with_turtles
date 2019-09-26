import turtle as t
import random as r
import time
from typing import Tuple, Optional

""" Return a box in top left bottom right corner form from a center
width and height.
"""


def box_centered_at(center, width, height):
    top_left = (center[0] - width // 2, center[1] + height // 2)
    bottom_right = (center[0] + width // 2, center[1] - height // 2)
    return top_left, bottom_right


""" Returns a tuple of two points representing the top left 
and top right of a box respectively.

:param area: is a box in the same for as the output specifying the area where 
the box can be centered.
:param max_h: is the max height of the box.
:param max_w: is the max width of the box.
"""


def rand_box(area: Tuple[Tuple[int, int], Tuple[int, int]], max_h: int,
             max_w: int, not_origin: bool = False) -> \
             Tuple[Tuple[int, int], Tuple[int, int]]:
    center = (r.randint(area[0][0], area[1][0]),
              r.randint(area[1][1], area[0][1]))
    height = r.randint(1, max_h)
    width = r.randint(1, max_w)
    box = box_centered_at(center, width, height)
    if not_origin:
        if intersects((0, 0), box):
            return rand_box(area, max_h, max_w, True)
        else:
            return box
    else:
        return box


""" Returns true if a box intersects with a point
"""


def intersects(point, box):
    return (box[0][0] <= point[0] <= box[1][0]
            and box[1][1] <= point[1] <= box[0][1])


def get_none_intersecting_point(boxes, area):
    point = (r.randint(area[0][0], area[1][0]),
             r.randint(area[1][1], area[0][1]))
    for box in boxes:
        if intersects(point, box):
            return get_none_intersecting_point(boxes, area)
    return point


class Simulator:
    """
    Simulator for turtle escape.
    Should only run one simulation at a time.
    """
    def __init__(self,
                 area=((-300, 300), (300, -300)),
                 max_h=100,  # max height a box can have
                 max_w=100,  # max width a box can have
                 num_boxes=30,
                 box_color="black",
                 target_size=10,
                 target_color="green",
                 box_draw_speed=10,
                 boxes=[],
                 target=(0, 0)):
        self._num_steps_forward = 0
        self._failed = False
        self._reached_target = False
        self._boxes = boxes
        self._target_box = None
        self._target = target

        self.wn = t.Screen()
        self.t = t.Turtle()

        self._area = area
        self.max_h = max_h
        self.max_w = max_w
        self.num_boxes = num_boxes
        self.box_color = box_color
        self.target_size = target_size
        self.target_color = target_color
        self.box_draw_speed = box_draw_speed

    def _draw_box(self, box, color="black"):
        old_color = self.t.fillcolor()
        old_speed = self.t.speed()
        self.t.speed(self.box_draw_speed)
        self.t.fillcolor(color)
        self.t.setpos(box[0])
        self.t.begin_fill()
        self.t.setpos((box[0][0], box[1][1]))
        self.t.setpos(box[1])
        self.t.setpos((box[1][0], box[0][1]))
        self.t.end_fill()
        self.t.fillcolor(old_color)
        self.t.speed(old_speed)

    """ Run one simulation
    Return number of steps the turtle took forward to reach the target or None
    if the turtle falls to reach the exit.
    @:param delay: The amount of time to wait between steps defaults to 1
    @:param new_environment: create a new target and new boxes.
    """
    def simulate(self, delay=1, new_environment=True) -> Optional[int]:
        self._num_steps_forward = 0
        self._failed = False
        self._reached_target = False

        # Generate random boxes and target for new env
        if new_environment:
            self._boxes = [rand_box(self._area,
                                    self.max_h,
                                    self.max_w,
                                    not_origin=True)
                           for _ in range(0, self.num_boxes)]

            self._target = get_none_intersecting_point(self.boxes, self._area)
        # clear the screen
        self.t.clear()
        # Paint all the boxes
        self.t.penup()
        for box in self.boxes:
            self._draw_box(box, self.box_color)
        # draw target
        self._draw_box(self.target_box, self.target_color)
        # Return to the origin
        self.t.setposition(0, 0)
        self.t.setheading(0)
        self.t.pendown()

        # for killing sim if turtle does not move
        last_pos = None
        last_angle = None
        # Simulation loop
        self.setup()
        while not self._failed and not self._reached_target:
            time.sleep(delay)
            self.update()
            pos = self.t.position()

            # Check intersection with boxes
            # Check if we haven't moved
            if pos == last_pos and self.t.heading() == last_angle:
                print("Motion less... making soup.")
                return None

            last_pos = pos
            last_angle = self.t.heading()

        if self._failed:
            return None
        return self._num_steps_forward

    def exit(self):
        self.wn.bye()

    def left(self, n: int) -> None:
        self.t.left(n)

    def right(self, n: int) -> None:
        self.t.right(n)

    def forward(self) -> None:
        self._num_steps_forward += 1
        self.t.forward(1)
        pos = self.t.position()
        for box in self._boxes:
            if intersects(self.t.position(), box):
                print("Hit box!")
                self._failed = True
        if not intersects(self.t.position(), self._area):
            print("Left area!", pos)
            self._failed = True
        # Check if we have reached the target
        if intersects(pos, self.target_box):
            self._reached_target = True

    def setup(self):
        raise NotImplementedError("You need to implement setup")

    def update(self):
        raise NotImplementedError("You need to implement update")

    @property
    def area(self):
        return self._area

    @property
    def boxes(self):
        return self._boxes

    @property
    def position(self):
        return self.t.position()

    @property
    def angle(self):
        return self.t.heading()

    @property
    def target(self):
        return self._target

    @property
    def target_box(self):
        return box_centered_at(self.target, self.target_size, self.target_size)
