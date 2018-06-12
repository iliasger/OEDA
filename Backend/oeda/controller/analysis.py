from flask_restful import Resource
from oeda.databases import db
from oeda.analysis.analysis_execution import get_tuples
from flask import jsonify, request
from elasticsearch.exceptions import TransportError
from oeda.log import *

class AnalysisController(Resource):

    @staticmethod
    def post(experiment_id, step_no):
        if experiment_id is None:
            return {"error": "experiment_id cannot be null"}, 404

        # as we only have one considered_data_type
        # naming conventions
        test_name = "two-way-anova"
        test_results = {}
        try:
            res = db().get_analysis(experiment_id, step_no, test_name)
            if res:
                test_results[test_name] = res
                resp = jsonify(res)
                resp.status_code = 200
                return resp
            else:
                return {"message": "Cannot get analysis results"}, 404
        except TransportError:
            return {"message": "Analysis result does not exist in database, please conduct another experiment"}, 404