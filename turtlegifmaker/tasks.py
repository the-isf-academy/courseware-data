from pathlib import Path
from importlib import import_module
import csv
import sys
from invoke import task
from itertools import product
import logging
from gifmaker import makegif

log = logging.getLogger()

MODULE_NAMES = [
    'main',
    'drawing'
]

FUNCTION_NAMES = [
    'main',
    'draw'
]

helptext = {
    "rosterfile": "CSV file containing columns: output_name, package, main_module, main_function",
    "outdir": "Directory where results should be saved",
    "dryrun": "Import functions but do not run them or save the results",
}

@task(help=helptext)
def make_gifs(ctx, rosterfile, outdir='export', dryrun=False):
    """Makes all gifs for a roster of students. 
    The roster should have columns: output_name, package, main_module, main_function.
    All packages should be importable (e.g. on the current python path or in the local directory.
    If main_module or main_function are empty, this function will try with best guesses.
    """
    configure_logger(log)
    if dryrun:
        log.info("Starting dry run. Not actually running the gif functions.")
    else:
        log.info("Starting run, saving gifs at {}.".format(outdir))
    out = Path(outdir)
    if not out.exists():
        out.mkdir()
    reader = csv.reader(Path(rosterfile).open())
    for output_name, package, main_module, main_function in reader:
        log.debug("Starting {}".format(output_name))
        fn, md, fn_name = try_import(package, main_module, main_function)
        if dryrun: continue
        if fn:
            gifpath = (out / output_name).with_suffix('.gif')
            try:
                makegif(fn, gif_path=gifpath)
                log.info("Saved {}".format(gifpath))
            except:
                log.warn("{} (from {}.{}, to be saved as {}) crashed.".format(
                        fn_name, package, md, gifpath))

def try_import(package, module=None, function=None):
    "Gets a function if possible"
    modules = ([module] if module else []) + MODULE_NAMES
    functions = ([function] if function else []) + FUNCTION_NAMES
    for md, fn in product(modules, functions):
        try:
            module = import_module(package + '.' + md)
            target_fn = getattr(module, fn)
            log.debug("imported {} from {}.{}".format(fn, package, md))
            return target_fn, md, fn
        except (ImportError, AttributeError):
            pass
    log.warn("Could not find a function to import from package {}".format(package))
    return None, None, None

def configure_logger(log):
    "Makes the logger print to stdout, at DEBUG level, with a formatter"
    log.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    log.addHandler(handler)
