# -*- coding: utf-8 -*-
import sys
import string
import random
import binascii
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime
import time
from flask_cors import CORS
import urllib.parse
import logging
import json

from flask import Flask, request, jsonify, render_template, Response

from pyomo.environ import *

################## Global Vars ##################



#################################################




################## Functions Block ##################
# Above each function declaration, please write a comment mentioning the inputs, type of each input, and the names
# Same applies for required returned values

# Function names CANNOT be the same as the Flask function names used at the later block of code!

# Write your functions here:


# Example function: Inputs: W_max > number Outputs: model_list > list, ob_list > list
def sample_pyomo(W_max):
    A = ['hammer', 'wrench', 'screwdriver', 'towel']
    b = {'hammer':8, 'wrench':3, 'screwdriver':6, 'towel':11}
    w = {'hammer':5, 'wrench':7, 'screwdriver':4, 'towel':3}
    # W_max= 14
    model = ConcreteModel()
    model.x = Var(A, within=Binary)
    model.value = Objective(expr = sum([b[i]*model.x[i] for i in A]),
                        sense=maximize)
    model.weight = Constraint(expr = sum([ w[i]*model.x[i] for i in A ]) <= W_max)
    opt = SolverFactory("glpk")
    result_obj = opt.solve(model, tee=True)
    result_obj.write()
    model.solutions.load_from(result_obj)
    ob_list = []
    model_list = []
    for ob in A:
        print(ob, model.x[ob].value)
        ob_list.append(ob)
        model_list.append(model.x[ob].value)
    return model_list, ob_list

#####################################################



app = Flask(__name__)
# To be used once core backend is deployed. Keeping open CORS for others to be able to test the API.
# cors = CORS(app, resources={r"/*": {"origins": "*.starke.services"}}, send_wildcard=True)
cors = CORS(app, resources={r"/*": {"origins": "*"}}, send_wildcard=True)


logging.getLogger('flask_cors').level = logging.ERROR


@app.route('/', methods=['GET'])
def health_stat():
    return Response(response=json.dumps({"Status": "All Good Here!"}),
                    status=200,
                    mimetype='application/json')


@app.route('/data_test2', methods=['POST'])
def data_test2():
    data = request.get_json()
    # request data
    W_max = data['W_max']

    model_list, ob_list = sample_pyomo(W_max)

    # response data
    res = {"values": model_list, "obs": ob_list}
    return Response(response=json.dumps({"result": res}),
                    status=200,
                    mimetype='application/json')

app.debug = False
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)


