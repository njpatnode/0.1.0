from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from shop.models import Controller
import json
from shop.result_functions import result_function
import pandas as pd

def analysis_controller_detail(request, analysis_controller_id):
    template_context = {}
    render(request, 'shop/analysis_controller/analysis_controller_detail.html', template_context)

### Helper Utility
def strip_controller_id(controller_id):
    return int(str(controller_id).replace("controller_", ""))

### AJAX Result Handler ####
def ajax_handler(request, trigger_controller_id):
    if request.method == 'GET':
        current_controller_values_json = request.GET.dict()
        result = result_handler(trigger_controller_id, current_controller_values_json)
        return HttpResponse(json.dumps(str(result)), content_type = "application/json") #current_controller_values_json
        #return HttpResponse(json.dumps(result), content_type = "application/json")


#### Generic Result Handler ####
def result_handler(trigger_controller_id, current_controller_values_json):
    trigger_controller_id = strip_controller_id(trigger_controller_id)
    trigger_controller = get_object_or_404(Controller, pk=trigger_controller_id)
    # Set up context
    #current_controller_values_json = str(current_controller_values_json)
    #parsed_json = json.loads(current_controller_values_json)
    keyword_args = {}
    for controller_id in current_controller_values_json.keys():
        controller_pk = strip_controller_id(controller_id)
        controller = get_object_or_404(Controller, pk=controller_pk)
        controller_variable = controller.variable
        keyword_args[controller_variable] = current_controller_values_json[controller_id]
    panel = trigger_controller.panel
    result_function_name = panel.result_function_name
    dataview = panel.accordion.analysis.data_view
    dataview_df = pd.read_pickle('dataview/{}'.format(dataview.id))
    #Translate widget ids to function parameters and values
    #Only use widgets with same panel and analysis widget - assume that names are unique
    #Call result function
    keyword_args['dataview_df'] = dataview_df
    result_function_obj = result_function()
    result = getattr(result_function_obj, result_function_name)(**keyword_args)
    return result



