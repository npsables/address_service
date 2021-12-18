import os
import logging
import sys
# sys.path.append('..')
from flask import request, jsonify, Flask, render_template, session
from flask_api import status
from flask_cors import CORS

from src.config_api import ApiResponse, DetectRequest
# # import src.const as const
from src import app, db
from src.handler.address_handler import get_chain_address, push_chain_address, create_defautl, delele_address

CORS(app)
log = logging.getLogger()
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)




@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/createdefault', methods=["POST"])
def create_default_wallet():
    log.info('Starting Process....')
    if request.method == "POST":
        json_reg = request.get_json(force=True, silent=True)
        
        log.info('request info:{}'.format(request))
        log.info('json_reg:{}'.format(json_reg))

        if not json_reg:
            return ApiResponse(message="Invalid json"), status.HTTP_400_BAD_REQUEST
        result = create_defautl(json_reg, db)

        return result


@app.route('/getaddress', methods=["POST"])
def get_address():
    log.info('Starting Process....')
    if request.method == "POST":
        json_reg = request.get_json(force=True, silent=True)
        log.info('request info:{}'.format(request))
        log.info('json_reg:{}'.format(json_reg))

        if not json_reg:
            return ApiResponse(message="Invalid json"), status.HTTP_400_BAD_REQUEST

        address = json_reg['address']
        chain = json_reg['chain']

        log.debug("Address: {}".format(address))
        log.debug("Chain ID: {}".format(chain))

        req = DetectRequest(address=address, chain=chain)
        ok, msg = req.validate()
        if not ok:
            return ApiResponse(message=msg), status.HTTP_400_BAD_REQUEST

        result = get_chain_address(address, chain, db)
        return result


@app.route('/pushaddress', methods=["POST"])
def push_address():
    log.info('Starting Process....')
    if request.method == "POST":
        json_reg = request.get_json(force=True, silent=True)
        log.info('request info:{}'.format(request))
        log.info('json_reg:{}'.format(json_reg))

        if not json_reg:
            return ApiResponse(message="Invalid json"), status.HTTP_400_BAD_REQUEST

        address = json_reg['address']
        chain = json_reg['chain']
        child_address = json_reg['child_address']
        purpose = json_reg['purpose']

        log.debug("Address: {}".format(address))
        log.debug("Chain ID: {}".format(chain))

        req = DetectRequest(address=address, chain=chain)
        ok, msg = req.validate()
        if not ok:
            return ApiResponse(message=msg), status.HTTP_400_BAD_REQUEST

        result = push_chain_address(address, chain, purpose, child_address, db)
        return result


@app.route('/deleteaddress', methods=["POST"])
def del_address():
    log.info('Starting Process....')
    if request.method == "POST":
        json_reg = request.get_json(force=True, silent=True)
        log.info('request info:{}'.format(request))
        log.info('json_reg:{}'.format(json_reg))

        if not json_reg:
            return ApiResponse(message="Invalid json"), status.HTTP_400_BAD_REQUEST

        address = json_reg['address']
        chain = json_reg['chain']
        purpose = json_reg['purpose']

        log.debug("Address: {}".format(address))
        log.debug("Chain ID: {}".format(chain))

        req = DetectRequest(address=address, chain=chain)
        ok, msg = req.validate()
        if not ok:
            return ApiResponse(message=msg), status.HTTP_400_BAD_REQUEST
        result = delele_address(address, chain, purpose, db)

        return result
