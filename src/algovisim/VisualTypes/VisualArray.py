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
        self.buffer_type: ArrayAnimationType = "get"

        self.old_tab = copy.deepcopy(self.tab)
        self.old_tab_counter = Counter(self.old_tab)

        # self.arrow = Arrow(UP,DOWN)
        # self.arrow.shift()

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
        to_play = [Write(obj) for obj in self.buffer_animations]
        if self.buffer_type == "set":
            to_play.append(self._draw(now=False))
        self.scene.play(*to_play)  # Play buffered animations concurrently
        self.scene.play(*[FadeOut(obj) for obj in self.buffer_animations])
        self.buffer_animations = []

    def _add_to_buffer(self, animation, animation_type: ArrayAnimationType):
        if animation_type != self.buffer_type:
            self.flush_buffer()
            self.buffer_type = animation_type
        self.buffer_animations.append(animation)

    def __getitem__(self, i):
        if i < 0:
            i = len(self) + i
        box = self.box_around(i, i)
        self._add_to_buffer(box, "get")
        return self.tab[i]

    def __setitem__(self, i, x):
        if i < 0:
            i = len(self) + i
        box = self.box_around(i, i, "red")
        self._add_to_buffer(box, "set")
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
        random_tab = [i for i in range(7)]
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
