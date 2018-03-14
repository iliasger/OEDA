from colorama import Fore

from oeda.log import *
from oeda.rtxlib.execution import experimentFunction


def start_sequential_strategy(wf):
    """ executes all experiments from the definition file """
    info("> ExecStrategy   | Sequential", Fore.CYAN)
    wf.totalExperiments = len(wf.execution_strategy["knobs"])
    for knob in wf.execution_strategy["knobs"]:
        wf.setup_stage(wf, knob)
        experimentFunction(wf, {
            "knobs": knob,
            "ignore_first_n_samples": wf.primary_data_provider["ignore_first_n_samples"],
            "sample_size": wf.execution_strategy["sample_size"],
        })
