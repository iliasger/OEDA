from oeda.rtxlib.executionstrategy.ForeverStrategy import start_forever_strategy
from oeda.rtxlib.executionstrategy.StepStrategy import start_step_strategy
from oeda.rtxlib.executionstrategy.SelfOptimizerStrategy import start_self_optimizer_strategy
from oeda.rtxlib.executionstrategy.SequencialStrategy import start_sequential_strategy
from oeda.rtxlib.executionstrategy.RandomStrategy import start_random_strategy
from oeda.rtxlib.executionstrategy.MlrStrategy import start_mlr_mbo_strategy
from oeda.rtxlib.executionstrategy.ThreePhaseStrategy import start_three_phase_strategy

from oeda.log import *

from oeda.rtxlib.executionstrategy.UncorrelatedSelfOptimizerStrategy import start_uncorrelated_self_optimizer_strategy


def run_execution_strategy(wf):
    """ we run the correct execution strategy """
    applyInitKnobs(wf)
    # start the right execution strategy
    if wf.analysis["type"] == "3_phase":
        start_three_phase_strategy(wf)

    elif wf.execution_strategy["type"] == "sequential":
        # log_results(wf.folder, wf.execution_strategy["knobs"][0].keys() + ["result"], append=False)
        start_sequential_strategy(wf)

    elif wf.execution_strategy["type"] == "self_optimizer":
        # log_results(wf.folder, wf.execution_strategy["knobs"].keys() + ["result"], append=False)
        start_self_optimizer_strategy(wf)

    elif wf.execution_strategy["type"] == "uncorrelated_self_optimizer":
        # log_results(wf.folder, wf.execution_strategy["knobs"].keys() + ["result"], append=False)
        start_uncorrelated_self_optimizer_strategy(wf)

    elif wf.execution_strategy["type"] == "step_explorer":
        # log_results(wf.folder, wf.execution_strategy["knobs"].keys() + ["result"], append=False)
        start_step_strategy(wf)

    elif wf.execution_strategy["type"] == "forever":
        start_forever_strategy(wf)

    elif wf.execution_strategy["type"] == "mlr_mbo":
        start_mlr_mbo_strategy(wf)

    # finished
    info(">")
    applyDefaultKnobs(wf)


def applyInitKnobs(wf):
    """ we are done, so revert to default if given """
    if "pre_workflow_knobs" in wf.execution_strategy:
        try:
            info("> Applied the pre_workflow_knobs")
            wf.change_provider["instance"] \
                .applyChange(wf.change_event_creator(wf.execution_strategy["pre_workflow_knobs"]))
        except:
            error("apply changes did not work")


def applyDefaultKnobs(wf):
    """ we are done, so revert to default if given """
    if "post_workflow_knobs" in wf.execution_strategy:
        try:
            info("> Applied the post_workflow_knobs")
            wf.change_provider["instance"] \
                .applyChange(wf.change_event_creator(wf.execution_strategy["post_workflow_knobs"]))
        except:
            error("apply changes did not work")
