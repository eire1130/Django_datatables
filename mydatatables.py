'''
Created on Feb 2, 2012

@author: jreynolds
'''
import datatables
from pricing.pricer.models.stores import PN



class Example(datatables.DataTables):
    model = PN
    class Media:
        js = ('/media/plugins/datatables/media/js/jquery.dataTables.min.js',
              '/media/plugins/datatables/extras/ColVis/media/js/ColVis.min.js',
              '/media/plugins/datatables/extras/ColReorder/media/js/ColReorder.min.js',)
    class Meta:
        params = (
                  ("bProcessing", True),
                  ("sAjaxSource", '/ajax/'),
                  ("bServerSide", True),
                  ("bDeferRender", True),
                  ("bJQueryUI", True),
                  ("bStateSave", True),
                  )
        template = 'json_file.txt'
        index = (('Policy','pn',True,),
                 ('Person','persons__last_name',True,),
                 ('Date of Birth','persons__dob',True,),)