from rest_framework import renderers
import json

class UserRenderer(renderers.JSONRenderer):
  charset='utf-8'
  def render(self, data, accepted_media_type=None, renderer_context=None):

    response = {
      "error":False,
      "status_code":renderer_context['response'].status_code,
      "message":"",
      "data":None,
      
    }
    if 'errors' in data.keys():
      response['error'] = True
      response['message'] = ' '.join([str(elem) for elem in data['errors']['non_field_errors']])
    elif 'detail' in data.keys():
      response['error'] = True
      response['message'] = "Invalid Token or Token Type"
    else:
      if "msg" in data.keys():
        response["message"] = data['msg']
        del data['msg']
      response["data"] = data
    
    return json.dumps(response)