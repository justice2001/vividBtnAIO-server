from django.http import HttpResponse
import json


def response_json(data, status=200):
    response = HttpResponse(json.dumps(data), content_type='application/json', status=status)
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response['Access-Control-Max-Age'] = '1000'
    response['Access-Control-Allow-Headers'] = '*'
    return response
