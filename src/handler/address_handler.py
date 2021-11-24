from re import purge
from flask import jsonify
# from src.config_api import DetectResult

def get_chain_address(address, chain, db):
    if address is None or chain is None:
        return jsonify(
        statusCode=400,
        message='Bad request',
        errors='No master address and chain ID'
    ), 400

    try: 
        a = list(db.address.find(
            {"_id": address}, {"_id": 0, "address": 1}))
        list_address=a[0]["address"][chain]

    except IndexError:
        return jsonify(
            statusCode=205,
            status='Fail',
            list_address=[],
            message='No data of ' + address,
        ), 205

    except:
        return jsonify(
            statusCode=205,
            status='Fail',
            list_address=[],
            message='No data of ' + address,
        ), 205
    # print("SEULTASERAWRAW", a)
    return jsonify(
        statusCode=201,
        message='Succeed',
        status='Succeed',
        list_address=list_address
    ), 200


def push_chain_address(address, chain, purpose, child_address, db):
    if address is None or chain is None or purpose is None or child_address is None:
        return jsonify(
        statusCode=400,
        message='Bad request',
        errors='Missing values'
    ), 400

    db.address.update(
        {"_id": address},
        {"$set": {
            f"address.{chain}.{purpose}": child_address
        }}
    )

    return jsonify(
        statusCode=201,
        message='Succeed',
    ), 200


def create_defautl(request, db):
    print(request)
    db.address.insert(request)

    return jsonify(
        statusCode=201,
        message='Succeed',
    ), 200

#     {
#     "_id": "test_default",
#     "address": {
#         "1": {
#             "default": "wallet1"
#         },
#         "60": {
#             "default": "wallet2"
#         },
#         "501": {
#             "default": "wallet3"
#         }
#     }
# }

def delele_address(address, chain, purpose, child_address, db):
    if address is None or chain is None or purpose is None or child_address is None:
        return jsonify(
        statusCode=400,
        message='Bad request',
        errors='Missing values'
    ), 400

    db.address.update({ "_id": address }, { "$unset" : { f"address.{chain}.{purpose}" : 1} })
    return jsonify(
        statusCode=201,
        message='Succeed',
    ), 200

