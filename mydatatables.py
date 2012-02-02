'''
Created on Feb 2, 2012

@author: jreynolds
'''
import datatables
from pricing.pricer.models.stores import PN



class Example(datatables.DataTables):
    model = PN
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