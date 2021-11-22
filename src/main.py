import os
import logging
import sys
# sys.path.append('..')
from flask import request, jsonify, Flask, render_template, session
from flask_api import status

from src.config_api import ApiResponse, DetectRequest
# # import src.const as const
from src import app, db
from src.handler.address_handler import get_chain_address, push_chain_address, create_defautl, delele_address

log = logging.getLogger()
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
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
        # if result.code != const.CODE_DONE:
        #     if result.code == const.CODE_FILE_EXIST:
        #         return ApiResponse(success=True, code=result.code, message=result.message)
        #     log.info('Get Error....')
        #     return ApiResponse(success=False, message=result.message), status.HTTP_400_BAD_REQUEST
        # log.info('End Process')
        # return ApiResponse(success=True, code=result.code)
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

        # session['user_id'] = user_id
        log.debug("Chain ID: {}".format(chain))
        req = DetectRequest(address=address, chain=chain)

        ok, msg = req.validate()
        if not ok:
            return ApiResponse(message=msg), status.HTTP_400_BAD_REQUEST

        result = get_chain_address(address, chain, db)
        # if result.code != const.CODE_DONE:
        #     if result.code == const.CODE_FILE_EXIST:
        #         return ApiResponse(success=True, code=result.code, message=result.message)
        #     log.info('Get Error....')
        #     return ApiResponse(success=False, message=result.message), status.HTTP_400_BAD_REQUEST
        # log.info('End Process')
        # return ApiResponse(success=True, code=result.code)
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

        # session['user_id'] = user_id
        log.debug("Chain ID: {}".format(chain))
        req = DetectRequest(address=address, chain=chain)

        ok, msg = req.validate()
        if not ok:
            return ApiResponse(message=msg), status.HTTP_400_BAD_REQUEST

        result = push_chain_address(address, chain, purpose, child_address, db)
        # if result.code != const.CODE_DONE:
        #     if result.code == const.CODE_FILE_EXIST:
        #         return ApiResponse(success=True, code=result.code, message=result.message)
        #     log.info('Get Error....')
        #     return ApiResponse(success=False, message=result.message), status.HTTP_400_BAD_REQUEST
        # log.info('End Process')
        # return ApiResponse(success=True, code=result.code)
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
        child_address = json_reg['child_address']
        purpose = json_reg['purpose']
        log.debug("Address: {}".format(address))

        # session['user_id'] = user_id
        log.debug("Chain ID: {}".format(chain))
        req = DetectRequest(address=address, chain=chain)

        ok, msg = req.validate()
        if not ok:
            return ApiResponse(message=msg), status.HTTP_400_BAD_REQUEST

        result = delele_address(address, chain, purpose, child_address, db)
        # if result.code != const.CODE_DONE:
        #     if result.code == const.CODE_FILE_EXIST:
        #         return ApiResponse(success=True, code=result.code, message=result.message)
        #     log.info('Get Error....')
        #     return ApiResponse(success=False, message=result.message), status.HTTP_400_BAD_REQUEST
        # log.info('End Process')
        # return ApiResponse(success=True, code=result.code)

        return result 