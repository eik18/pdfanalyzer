#!/usr/bin/which python
import re
class pdfanalysis():
    def __init__(self,filename):
        try:
            fileobject=open(filename,"rb")
            self.resultstring=fileobject.read()
            self.messaging_queue=[]
            
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
                location=int(location)
                if self.resultstring[location:location+5]!='xref\n':
                    xref_location_error['error']=True
                    xref_location_error['msg']='xref not in expected location'
                    break
                else:
                    xref_location_error['error']=False
                    xref_location_error['msg']='xref\'s in expected locations'
        elif num_xref==0:
            xref_location_error['error']=True
            xref_location_error['msg']='xref locations not found'
        self.messaging_queue.append(xref_location_error)
        
        #print xref_location_error
        #validate xref content
    def mapxref(self):
        xref_content_error={'error':False,'msg':''}
        xref_contents_array=re.findall('(?<=xref\n)[\s,\d,fn]+(?=\ntrailer\n)',self.resultstring)
        xref_count={'xref_obj_count':0,'actual_obj_count':0,'xref_pointers':[]}

        if xref_contents_array:
            for item in xref_contents_array:
                temparray=item.split('\n')
                for line in temparray:
                    if re.match('^\d+?\s\d+?$',line):
                        templine=line.strip()
                        xref_parts=templine.split(' ')
                        if len(xref_parts) >2:
                            xref_content_error={'error':True,'msg':'xref contents index malformed'}
                        else:
                            if xref_parts[1].isdigit(): xref_count['xref_obj_count']=int(xref_parts[1])+xref_count['xref_obj_count']
                    elif re.match('0000000000 65535 f',line):
                        xref_count['actual_obj_count']=1+xref_count['actual_obj_count']
                    elif re.match('^\d+? \d+? n',line):
                        templine=line.strip()
                        xref_parts=templine.split(' ')
                        if xref_parts[0].isdigit():
                            xref_count['actual_obj_count']=1+xref_count['actual_obj_count']
                            xref_count['xref_pointers'].append(int(xref_parts[0]))
                    else:
                        xref_content_error={'error':True,'msg':'xref contents index malformed'}
            print xref_count
        else: 
            xref_content_error={'error':True,'msg':'Xref contents not found'}
        self.messaging_queue.append(xref_content_error)
            
'''add re.findall('(?<=\d \d obj\n)[\S\s]*?(?=endobj)',string)


'''
         


def main():
    item=pdfanalysis("contract.pdf")
    item.process_xref()
    item.mapxref()
    

if __name__=='__main__':
    main()