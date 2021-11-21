from re import purge
from flask import jsonify
import src.main


def get_chain_address(address, chain, db):
    a = list(db.address.find(
        {"_id": address}, {"_id": 0, "address": 1}))

    # print("SEULTASERAWRAW", a)
    return jsonify(
        statusCode=201,
        message='Succeed',
        coin=a[0]["address"][chain]
    ), 200


def push_chain_address(address, chain, purpose, child_address, db):
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
    db.address.update({ "_id": address }, { "$unset" : { f"address.{chain}.{purpose}" : 1} })
    return jsonify(
        statusCode=201,
        message='Succeed',
    ), 200

