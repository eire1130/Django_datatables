'''
Created on Feb 1, 2012

@author: jreynolds
'''
from django.db.models import Q
from django.utils import simplejson
from django.template.loader import render_to_string
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.forms.widgets import media_property

class ModelTableOptions(object):
    def __init__(self, options=None):
        self.params = getattr(options, 'params', None)
        self.template = getattr(options, 'template', None)
        self.index = getattr(options, 'index', None)





class DataTablesMetaclass(type):
    def __new__(cls, name, bases, attrs):
        try:
            parents = [b for b in bases if issubclass(b, DataTables)]
        except NameError:
            parents = None
        new_class = super(DataTablesMetaclass, cls).__new__(cls, name, bases,
                attrs)
        if not parents:
            return new_class
        if 'media' not in attrs:
            new_class.media = media_property(new_class)
        opts = new_class._meta = ModelTableOptions(getattr(new_class, 'Meta', None))
        try:
            declared_params = dict(opts.params)
        except TypeError:
            declared_params = {}
        try:
            jsonTemplatePath = opts.template
        except TypeError:
            jsonTemplatePath = None
            
            
        try:
            index = map(lambda x: x[1], opts.index)
            columnIndexNameMap = dict(zip(range(len(index)),index))
        except TypeError:
            columnIndexNameMap = None
        try:
            MyColumnNames = map(lambda x: x[0], opts.index)
            #columnIndexNameMap = dict(zip(range(len(index)),index))
        except TypeError:
            columnIndexNameMap = None

        try:
            searchableColumns = map(lambda y: y[1], filter(lambda x: x[2],opts.index)) #list(opts.search)
        except TypeError:
#            try:
#                searchableColumns = list(opts.index)
#            except TypeError:
            searchableColumns = None
            
            
        new_class.declared_params = declared_params
        new_class.jsonTemplatePath = jsonTemplatePath
        new_class.columnIndexNameMap = columnIndexNameMap
        new_class.searchableColumns = searchableColumns
        new_class.MyColumnNames = MyColumnNames
        return new_class
    

class BaseDataTables(object):
    queryset = None
    model = None

    def __init__(self):
        self.js = simplejson.dumps(self.declared_params)

        if self.model != None:
            self.queryset = self.model.objects.all()
    def __unicode__(self):
        return self.js


    def get_table(self, _id, css_class, border=0, cellspacing=0,cellpadding=0):
        table = u'''<table cellpadding="{4}" cellspacing="{3}" border="{2}" class="{0}" id="{1}" style="width:100%;">\n'''.format(css_class,_id,border,cellspacing,cellpadding)
        end_table =  u'''</table>'''
        begin = u'\t\t\t<th>{0}</th>\n'
        all_th = u'\t<thead>\n\t\t<tr>\n'
        for column in self.MyColumnNames:
            all_th += begin.format(column)
        all_th +=u'\t\t</tr>\n\t</thead>\n'
        return mark_safe(force_unicode(table + all_th + u'''\t<tbody>\n''' + u'''\t</tbody>\n''' + end_table))
    
    
    def get_datatables_records(self, request, *args):
        querySet = self.queryset
        #Safety measure. If someone messes with iDisplayLength manually, we clip it to
        #the max value of 100.
        if not 'iDisplayLength' in request.GET or not request.GET['iDisplayLength']:
            iDisplayLength = 10 # default value
        else: 
            iDisplayLength = min(int(request.GET['iDisplayLength']),100)
    
        if not 'iDisplayStart' in request.GET or not request.GET['iDisplayStart']:
            startRecord = 0 #default value
        else:
            startRecord = int(request.GET['iDisplayStart'])
        endRecord = startRecord + iDisplayLength 
    
        #apply ordering 
        if not 'iSortingCols' in request.GET or not request.GET['iSortingCols']:
            iSortingCols = 0 #default value
        else:
            iSortingCols = int(request.GET['iSortingCols'])
        asortingCols = []
        
        if iSortingCols>0:
            for sortedColIndex in range(0, iSortingCols):
                sortedColName = self.columnIndexNameMap[int(request.GET['iSortCol_'+str(sortedColIndex)])]
                sortingDirection = request.GET['sSortDir_'+str(sortedColIndex)]
                if sortingDirection == 'desc':
                    sortedColName = '-'+sortedColName
                asortingCols.append(sortedColName) 
                
            querySet = querySet.order_by(*asortingCols).distinct()
        
        #apply filtering by value sent by user
        if not 'sSearch' in request.GET or not request.GET['sSearch']:
            customSearch = '' #default value
        else:
            customSearch = str(request.GET['sSearch'])
        if customSearch != '':
            outputQ = None
            first = True
            for searchableColumn in self.searchableColumns:
                kwargz = {searchableColumn+"__icontains" : customSearch}
                q = Q(**kwargz)
                if (first):
                    first = False
                    outputQ = q
                else:
                    outputQ |= q
            querySet = querySet.filter(outputQ)
            
        #count how many records match the final criteria
        iTotalRecords = iTotalDisplayRecords = querySet.count()
        
        #get the slice
        querySet = querySet[startRecord:endRecord]
        
        #prepare the JSON with the response
        if not 'sEcho' in request.GET or not request.GET['sEcho']:
            sEcho = '0' #default value
        else:
            sEcho = request.GET['sEcho'] #this is required by datatables 
        jsonString = render_to_string(self.jsonTemplatePath, locals())
        return jsonString
        #return HttpResponse(jsonString, mimetype="application/javascript")
        

    
class DataTables(BaseDataTables):
    __metaclass__ = DataTablesMetaclass



if __name__ == '__main__':
    
    pass
