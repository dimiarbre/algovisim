# ALGOVISIM
A tool to visualize basic data structures operations.
Aimed to provide student with a visual way to figure out algorithms.


## Installation
You should have `pixi` installed, see [their documentation](https://pixi.sh/dev/). Then, running `pixi install` should suffice.
This project heavily relies on Manim, see [their documentation](https://docs.manim.community/en/stable/tutorials/quickstart.html).
If you use the VSCode [Manim sideview](https://marketplace.visualstudio.com/items?itemName=Rickaym.manim-sideview) extension to compile, and you get an error `Unknown encoder 'libx264'`, or `Error selecting an encoder`, 
you can either fix this by installing the library globally, or try to launch VSCode from a pixi environment: `pixi run code .`

## Contributing:
Consider using `black` and `isort`. It should be installed via pixi, but remember to format before committing. You can configure most editors to format on save.


## ROADMAP
- [ ] Have visualization structures
    - [ ] Table implementation
    - [ ] Implement Tree algorithms
    - [ ] Graph data structure.
- [ ] Example algorithms
    - [ ] Search algorithms
    - [ ] Sorting algorithms
- [ ] Have code structure
    - [ ] Adapt data structure to other languages (Python, C?, OCaml?)
    - [ ] Parse simple programs to python meta-execution, and run code in parallel to highlight the flow the code.
 