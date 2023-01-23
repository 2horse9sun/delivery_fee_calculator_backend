from pymongo import MongoClient


def success_response(data = ''):
    return {
        "data": data,
        "status_code": 0
    }

  
def error_response(error, status_code = -1):
    return {
        "error": str(error),
        "status_code": status_code
    }