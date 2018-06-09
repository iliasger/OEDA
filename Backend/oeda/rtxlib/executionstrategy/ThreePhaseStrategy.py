from colorama import Fore
from oeda.log import *
from oeda.rtxlib.execution import experimentFunction
from oeda.analysis.analysis_execution import start_factorial_tests
from oeda.databases import db
from oeda.rtxlib.executionstrategy.StepStrategy import start_step_strategy
from oeda.analysis.analysis_execution import get_tuples, delete_combination_notation, \
                                             iterate_anova_tables, get_significant_interactions

import pprint
pp = pprint.PrettyPrinter(indent=4)

def start_three_phase_strategy(wf):
    """ executes ANOVA, bayesian opt, and Ttest """
    info("> ExecStrategy   | 3Phase", Fore.CYAN)

    info("> Starting experimentFunction for ANOVA")
    start_step_strategy(wf)

    info("> Starting ANOVA")
    # as we have only one data type, e.g. overhead
    considered_data_type_name = wf.considered_data_types[0]["name"]
    wf.analysis["data_type"] = considered_data_type_name
    successful, aov_table, aov_table_sqr = start_factorial_tests(wf)

    if successful:
        stage_ids, samples, knobs = get_tuples(wf.id, considered_data_type_name)
        all_res = db().get_analysis(experiment_id=wf.id, stage_ids=stage_ids, analysis_name='two-way-anova')
        # now we want to select the most important factors out of anova result, following can also be integrated
        # aov_table = aov_table[aov_table["omega_sq"] > min_effect_size]
        sorted_significant_interactions = get_significant_interactions(all_res["anova_result"], wf.analysis["anovaAlpha"], wf.analysis["nrOfImportantFactors"])
        # in this case, we can't find any significant interactions
        if sorted_significant_interactions is None:
            db().update_analysis(experiment_id=wf.id, stage_ids=stage_ids, analysis_name='two-way-anova', field='eligible_for_next_step', value=False)
            return
        else:
            db().update_analysis(experiment_id=wf.id, stage_ids=stage_ids, analysis_name='two-way-anova', field='eligible_for_next_step', value=True)
            # TODO: proceed to BOGP execution
            return
    else:
        error("> ANOVA failed")

    info(">")