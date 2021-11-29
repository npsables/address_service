from re import purge
from flask import jsonify
from src.util import checker
# from src.config_api import DetectResult

def get_chain_address(address, chain, db):
    if address is None or chain is None:
        return jsonify(
        statusCode=400,
        message='Bad request',
        list_address=[],
        errors='No master address and chain ID'
    ), 400

    try: 
        a = list(db.address.find(
            {"_id": address}, {"_id": 0, "address": 1}))
        list_address=a[0]["address"][chain]

    except IndexError:
        return jsonify(
            statusCode=400,
            status='Fail',
            list_address=[],
            message='No data of ' + address + ", try another chainID or address",
        ), 400

    except KeyError:
        return jsonify(
            statusCode=400,
            status='Fail',
            list_address=[],
            message='Not supported, try another chainID or address',
        ), 400

    except Exception as e:
        return jsonify(
            statusCode=400,
            status='Unknown',
            list_address=[],
            message=e,
        ), 400


    # print("SEULTASERAWRAW", a)
    return jsonify(
        statusCode=200,
        message='Succeed',
        status='Succeed',
        list_address=list_address
    ), 200


def push_chain_address(address, chain, purpose, child_address, db):
    if address is None or chain is None or purpose is None or child_address is None:
        return jsonify(
        statusCode=400,
        message='Missing values',
    ), 400

    try:
        db.address.update(
            {"_id": address},
            {"$set": {
                f"address.{chain}.{purpose}": child_address
            }}
        )
    except Exception as e:
        return jsonify(
            statusCode=1003,
            status='Cant not update',
            message=e,
        ), 1003

    return jsonify(
        statusCode=200,
        message='Succeed',
    ), 200


def create_defautl(request, db):
    print(request)
    # parse, ok = checker.parse_default(request)
    # if not ok:

    _id = request['address']
    checker =list(db.address.find({"_id": _id}))
    # print("CHECKER ", checker)

    if checker != []:
        return jsonify(
            statusCode=1005,
            status='Refused',
            message="Master address already exist",
        ), 500

    try:
        db.address.insert(request)
    except Exception as e:
        return jsonify(
            statusCode=1003,
            status='Cant not update',
            message=e,
        ), 1003

    return jsonify(
        statusCode=200,
        message='Succeed',
    ), 200


def delele_address(address, chain, purpose, child_address, db):
    if address is None or chain is None or purpose is None or child_address is None:
        return jsonify(
        statusCode=400,
        message='Bad request',
        errors='Missing values'
    ), 400
    try: 
        db.address.update({ "_id": address }, { "$unset" : { f"address.{chain}.{purpose}" : 1} })
    except Exception as e:
        return jsonify(
            statusCode=1003,
            status='Cant not update',
            message=e,
        ), 1003

    return jsonify(
        statusCode=200,
        message='Succeed',
    ), 200

