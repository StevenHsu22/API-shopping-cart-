from datetime import datetime


# def response(status, data=None):
#     if status:
#         message, http_code = "success", 200
#     else:
#         message, http_code = "failure", 500

#     ret = {"message": message}
#     if data is not None:
#         ret["data"] = data
#         ret["datatime"] = datetime.utcnow().isoformat()

#     return ret, http_code


def success(data=None, price=0):
    if data is None:
        return {'message': 'success'}, 200
        
    if price != 0:
        return {
        'message': 'success',
        'data': data,
        'total_price':price,
        'datatime': datetime.utcnow().isoformat()
    }, 200

    return {
        'message': 'success',
        'data': data,
        'datatime': datetime.utcnow().isoformat()
    }, 200




def failure(data=None):
    if data is not None:
        return {'message': 'failure'}, 500
    
    return {
        'message': 'failure',
        'data': data,
        'datatime': datetime.utcnow().isoformat()
    }, 500