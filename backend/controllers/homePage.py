from flask import jsonify, request

def getHome():
    return jsonify({
        "msg": "yay",
        "success": True
    })