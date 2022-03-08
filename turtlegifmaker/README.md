# turtlegifmaker
Provides the module and shell scripts needed to turn your python turtle drawing into a gif that animates the drawing process.

# Instructions for creating a gif from a single repo! 
0. You will need to install the Python Image Library (`pip install Pillow`). 

1. Import `gifmaker.py` into your animation repo. In `gifmaker.py`, replace `your_drawing_function` with your desired animation function and specify the gif name and path name. In the animation repo's `main.py`, make sure that (1) the animation ends up with `bye()` rather than `done()` or `input()` and (2) the screen is being set up at the beginning of the file (see code snippet below).

```
screen = Screen()
screen.setup(settings.SCREENWIDTH,settings.SCREENHEIGHT)
```


2. In terminal, run:   
```
python gifmaker.py
```


## Batch processing Command-line interface

```
Usage: inv[oke] [--core-opts] make-gifs [--options] [other tasks here ...]

Docstring:
  Makes all gifs for a roster of students. 
  The roster should have columns: output_name, package, main_module, main_function.
  All packages should be importable (e.g. on the current python path or in the local directory.
  If main_module or main_function are empty, this function will try with best guesses.

Options:
  -d, --dryrun                     Import functions but do not run them or save the results
  -o STRING, --outdir=STRING       Directory where results should be saved
  -r STRING, --rosterfile=STRING   CSV file containing columns: output_name, package, main_module, main_function
```

You will need [invoke](http://www.pyinvoke.org/) installed (`pip install invoke`). Then you can run `inv --list` to see 
available tasks and `inv --help make-gifs` for detailed help on the `make-gifs`
task. 

Essentially, this task is configured with a CSV file specifying each gif's
output name, package, main module, and main function. If you have all of the
student projects checked out in the same directory, each should be importable. 

You can also edit `MODULE_NAMES` and `FUNCTION_NAMES` in `tasks.py`. These are
the default names which are tried when attempting to import. If main module and 
main function are not specified for a given student, only these default guesses
are used.


# Credits
Written by [Jenny Han](https://github.com/jennylihan) and [Chris Proctor](https://github.com/cproctor/)

Code adapted from https://stackoverflow.com/questions/41319971/is-there-a-way-to-save-turtles-drawing-as-an-animated-gif/41353016#41353016
