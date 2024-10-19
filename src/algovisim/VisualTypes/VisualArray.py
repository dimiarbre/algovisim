import copy
import random
from collections import Counter
from typing import Literal

from manim import *

ArrayAnimationType = Literal["get", "set"]


class VisualArray(list):
    def __init__(self, tab: list[int], scene: Scene):
        self.tab = tab
        self.tab_object = Text(str(self.tab))
        self.scene = scene
        self.scene.play(Write(self.tab_object))
        self.nb_iterators = 0
        # Will buffer accesses of the same type to speed up and display concurrent accesses.
        self.buffer_animations = []
        self.buffer_clear = []  # Clearing animations, to make boxes and such dissapear.
        self.buffer_type: ArrayAnimationType = "get"

        self.old_tab = copy.deepcopy(self.tab)
        self.old_tab_counter = Counter(self.old_tab)

        self.arrow = None
        self.arrow_buffer = []

    def _draw(self, now=True) -> Transform:
        """Redraw the array, and try to make a permutation if possible.

        Args:
            now (bool, optional): If . Defaults to True.

        Returns:
            Transform: _description_
        """
        new_object = Text(str(self.tab))
        current_tab_counter = Counter(self.tab)
        if current_tab_counter == self.old_tab_counter:
            transform = TransformMatchingShapes(
                self.tab_object, new_object, path_arc=-PI
            )
        else:
            transform = Transform(self.tab_object, new_object)

        # Update old tab.
        self.tab_object = new_object
        self.old_tab = copy.deepcopy(self.tab)
        self.old_tab_counter = current_tab_counter
        return transform

    def __len__(self):
        return len(self.tab)

    def flush_buffer(self):
        # to_play = [Write(obj) for obj in self.buffer_animations]
        if self.buffer_type == "set":
            self.buffer_animations.append(self._draw(now=False))
        if len(self.buffer_animations) > 0:
            self.scene.play(
                *self.buffer_animations
            )  # Play buffered animations concurrently
        if len(self.buffer_clear) > 0:
            self.scene.play(*self.buffer_clear)
        self.buffer_animations = []
        self.buffer_clear = []

    def _add_to_buffer(
        self, animation, animation_type: ArrayAnimationType, clear_animation=None
    ):
        if animation_type != self.buffer_type:
            self.flush_buffer()
            self.buffer_type = animation_type
        if animation is not None:
            self.buffer_animations.append(animation)
        if clear_animation is not None:
            self.buffer_clear.append(clear_animation)

    def __getitem__(self, i):
        if i < 0:
            i = len(self) + i
        arrow_animation = self._new_arrow_position(i)
        self._add_to_buffer(arrow_animation, "get")
        return self.tab[i]

    def _new_arrow_position(self, i):
        if self.arrow is None:
            # When we draw an arrow for the first time
            self.arrow = Arrow(UP, DOWN)
            self.arrow.move_to(self.tab_object[self.get_true_index(i)])
            # TODO: have a consistent spacing by extracting the top coordinates
            self.arrow.shift(1.2 * UP)
            self.scene.add(self.arrow)
            return None
        else:
            new_arrow = Arrow(UP, DOWN)
            new_arrow.move_to(self.tab_object[self.get_true_index(i)])
            # TODO: have a consistent spacing by extracting the top coordinates
            new_arrow.shift(1.2 * UP)
            self.arrow.target = new_arrow
            return MoveToTarget(self.arrow)

    def __setitem__(self, i, x):
        if i < 0:
            i = len(self) + i
        box = self.box_around(i, i, "red")
        self._add_to_buffer(Write(box), "set", clear_animation=FadeOut(box))
        self.tab[i] = x

    def _index(self, i):
        if i < 0:
            i = len(self) + i
        return i

    def get_true_index(self, i):
        i = self._index(i)
        return 2 * i + 1

    def box_around(self, i, j, color="yellow"):
        i, j = self.get_true_index(i), self.get_true_index(j)
        i, j = min(i, j), max(i, j)
        box = SurroundingRectangle(self.tab_object[int(i) : int(j + 1)], color=color)
        return box


class VisualArrayExample(Scene):
    def construct(self):
        random.seed(421)
        random_tab = [i for i in range(10)]
        random.shuffle(random_tab)
        tab = VisualArray(random_tab, self)

        for j in range(len(tab)):
            for i in range(len(tab) - 1):
                if tab[i] > tab[i + 1]:
                    tab[i], tab[i + 1] = tab[i + 1], tab[i]
        tab.flush_buffer()


if __name__ == "__main__":

    scene = VisualArrayExample()
    scene.render()
