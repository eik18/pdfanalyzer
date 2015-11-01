#!/usr/bin/which python
import re
from matplotlib.cbook import Null
class pdfanalysis():
    def __init__(self,filename):
        try:
            fileobject=open(filename,"rb")
            self.resultstring=fileobject.read()
        except Exception as e:
            print "Whoops, problem importing file: {0}".format(e)

    def process_xref(self):
        #Find all the xref locations
        startxref_locations=re.findall('(?<=startxref\n)[\d]+',self.resultstring)
        num_xref=len(startxref_locations)
        
        #validate locations
        xref_location_error={'error':False,'msg':''}
        if num_xref >0:
            for location in startxref_locations:
                if self.resultstring[location:location+5]!='xref\n':
                    xref_location_error['error']=True
                    xref_location_error['msg']='xref not in expected location'
                    break
        elif num_xref==0:
            xref_location_error['error']=True
            xref_location_error['msg']='xref locations not found'
        else:
            xref_location_error['error']=False
            xref_location_error['msg']='xref\'s in expected locations'
        
        #validate xref content
        xref_contents=re.findall('(?<=xref\n)[\s,\d,fn]+(?=\ntrailer\n)',self.resultstring)
    def    

    def dumppdf(self):
        return self.resultstring


def main():
    exit()

if __name__=='__main__':
    main()