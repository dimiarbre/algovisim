from manim import *
import random


class VisualArray(list):
    def __init__(self, tab: list[int], scene: Scene):
        self.tab = tab
        self.tab_object = Text(str(self.tab))
        self.scene = scene
        self.scene.play(Write(self.tab_object))
        self.nb_iterators = 0

    def _draw(self):
        new_object = Text(str(self.tab))
        self.scene.play(Transform(self.tab_object, new_object))

    def __len__(self):
        return len(self.tab)

    def __getitem__(self, i):
        if i < 0:
            i = len(self) + i
        box = self.box_around(i, i)
        self.scene.play(FadeOut(box))
        return self.tab[i]

    def __setitem__(self, i, x):
        if i < 0:
            i = len(self) + i
        box = self.box_around(i, i, "red")
        self.tab[i] = x
        self._draw()
        self.scene.play(FadeOut(box))

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
        self.scene.play(Write(box))
        return box


class VisualArrayExample(Scene):
    def construct(self):
        random.seed(421)
        random_tab = [i for i in range(7)]
        random.shuffle(random_tab)
        tab = VisualArray(random_tab, self)

        x = tab[1]
        x = tab[-1]
        tab[-1] = 0

        for j in range(len(tab)):
            for i in range(len(tab) - 1):
                if tab[i] > tab[i + 1]:
                    tab[i], tab[i + 1] = tab[i + 1], tab[i]


if __name__ == "__main__":

    scene = VisualArrayExample()
    scene.render()
