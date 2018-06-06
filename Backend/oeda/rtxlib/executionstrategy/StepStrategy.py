from colorama import Fore
from oeda.log import *
from oeda.rtxlib.execution import experimentFunction
import itertools

def start_step_strategy(wf):
    """ implements the step strategy, a way to explore a hole feature area """
    info("> ExecStrategy   | Step", Fore.CYAN)

    # we look at the ranges and the steps the user has specified in the knobs
    knobs = wf.execution_strategy["knobs"]
    list_of_knobs = get_cartesian_product(knobs)
    wf.totalExperiments = len(list_of_knobs)
    info("> Steps Created  | Count: " + str(wf.totalExperiments), Fore.CYAN)
    for knob in list_of_knobs:
        step_execution(wf, knob)

def step_execution(wf, knob):
    """ runs a single step_execution experiment """
    debug("knob in step_execution" + str(knob), Fore.GREEN)
    # create a new experiment to run in execution
    exp = dict()
    exp["ignore_first_n_samples"] = wf.primary_data_provider["ignore_first_n_samples"]
    exp["sample_size"] = wf.execution_strategy["sample_size"]
    exp["knobs"] = knob
    wf.setup_stage(wf, exp["knobs"])
    return experimentFunction(wf, exp)


# ref: https://stackoverflow.com/questions/5228158/cartesian-product-of-a-dictionary-of-lists
def get_cartesian_product(knobs):
    keys, values = knobs.keys(), knobs.values()
    opts = [dict(zip(keys, items)) for items in itertools.product(*values)]
    return opts
