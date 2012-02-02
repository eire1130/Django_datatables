
from django.http import HttpResponse
from django.shortcuts import render_to_response
from mydatatables import Example


def listall(request):
    a = Example()
    table_id = "Example"
    table = a.get_table(table_id, "display")
    c = {'table':table,'table_id':table_id }
    return render_to_response('policylist.html', c)

def ajax(request):
    a = Example()
    json_string = a.get_datatables_records(request)
    return HttpResponse(json_string, mimetype="application/json")

def config(request):
    a = Example()
    return HttpResponse(a.js, mimetype="application/json")


if __name__ == '__main__':
    pass