= django_datatables =
django_datatables aims to simplify integration of the datatables jquery plugin, 
while providing a familiar API and adhering to DRY principals.
Most Datatables features should be accessible from within the Django / Python API.

== Acknowledgements ==
Lukasz Dziedzia and Pawel Roman for creating the get_datatables_records method.
http://www.assembla.com/code/datatables_demo/subversion/nodes/trunk/1_6_2

Inspiration from https://github.com/gerry/django-jqgrid


== Prerequisites ==
  * [http://www.jquery.com jQuery 1.7.1+]
  * [http://datatables.net/index Datatables 1.9+]

== Example ==

1. First create a new file someplace and create a new class inhereting from datatables.DataTables.

Defining the class is similar to Django Models and ModelForms.

{{{
    model = PN #a model can be defined directly, or a queryset can be defined using queryset = XXX. If both are defined, the model will override the queryset.
    class Meta:
		#Params is a tuple of two element tuples. These are the options taken from the Datatables options. If the second option is a dictionary, it should be here as well.
		#
        params = (
                  ("bProcessing", True),
                  ("sAjaxSource", '/ajax/'),
                  ("bServerSide", True),
                  ("bDeferRender", True),
                  ("bJQueryUI", True),
                  ("bStateSave", True),
                  )
		#template is simply the text file which will be used to generate your ajax. This should reside with the rest of your templates
        template = 'json_file.txt'
		#index is a tuple of three tuple elements. The first item is the Column name.
		# The second is what will be used to search following django search mecnaisms.
		#The third is you want to filter by this column
        index = (('Policy','pn',True,),
                 ('Person','persons__last_name',True,),
                 ('Date of Birth','persons__dob',True,),)
}}}


2. Create views to handle the non-ajax requests.
{{{
def listall(request):
    a = Example()
    table_id = "Example"
    table = a.get_table(table_id, "display")
    c = {'table':table,'table_id':table_id }
    return render_to_response('policylist.html', c)
}}}
{{{
3. Create views to handle the ajax requests.
def ajax(request):
    a = Example()
    json_string = a.get_datatables_records(request)
    return HttpResponse(json_string, mimetype="application/json")

def config(request):
    a = Example()
    return HttpResponse(a.js, mimetype="application/json")
}}}


4. Define urls for those views.
{{{
urlpatterns = patterns('myproject.views',

    url(r'^ajax/$', 'ajax',name='ajax'),
    url(r'^config/$', 'config',name='config'),
}}}

5. Configure jgrid to use the defined urls. Here I am using 
{{{
var osTable;
$(function(){

$.getJSON("{% url config %}",
			null,
			function( json ){
			osTable = $('#{{ table_id }}').dataTable(json);
			});
    			});
}}}

6. Configure the rest of the template:

Notice I am using the {{ table }} to generate the entire table. You can still write it out the headers manually, or if you requre more customization,
you can override the get_table method that generates the table.


{{{
	{% extends "base.html" %}



	{% block scripts %}

	<link rel="stylesheet" href="/media/plugins/datatables/media/css/jquery.dataTables_themeroller.css"/>
	<script type="text/javascript" src="/media/plugins/datatables/media/js/jquery.dataTables.js"></script>


	<script type="text/javascript">
	var osTable;
	$(function(){

	$.getJSON("{% url config %}",null,function( json ){
					osTable = $('#{{ table_id }}').dataTable(json);
					});
	});

	</script>
	{% endblock %}

	{% load pricing_features %}

	{% block containerstyle %}
		style = "width: 95%;"
	{% endblock %}

	{% block content %}

		{{ table }}

	{% endblock %}

}}}