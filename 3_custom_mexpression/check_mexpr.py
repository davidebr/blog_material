import sys, os
from schrodinger.application.desmond.enhsamp import parseStr
import schrodinger.application.desmond.cms as cms

mexpr_file=sys.argv[1]
cms_file=sys.argv[2]

print("M-expression file",mexpr_file)
print("CMS file ", cms_file)

with open(mexpr_file) as fh:
    m_expr = fh.read()
    model = cms.Cms(file=cms_file)
    #try: 
    s_expr = parseStr(model, m_expr)
    #print(s_expr)
    #except e:
    #   print("Your m-expression has some problems!")
 
