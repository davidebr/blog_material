from schrodinger.application.desmond import cmj
#BUG: this below is needed to load the stages because requires some global variable PARAM otherwise stages are not identified?
from schrodinger.application.desmond import stage

import schrodinger.application.desmond.cms as cms
import schrodinger.utils.sea as sea
from schrodinger.application.desmond import config 
from schrodinger.application.desmond.meta import parse_meta,generate_meta_cfg,CmsModel

from copy import deepcopy
from os import path
import sys
import argparse

def convert_meta_into_mexpression(mymsj,mycms):
    model = cms.Cms( file = mycms )
    parsed_file=cmj.parse_msj(mymsj)

    for i,p in enumerate(parsed_file): 
         if 'meta'  in p.param.keys():
                  meta_content=p.param['meta']
                  # if it has a cv defined then it must be a metadynamics run that we can parse
                  if hasattr(meta_content,'cv'):
                      meta = deepcopy(meta_content)
                      for cv in meta.cv:
                          new_atom = sea.List()
                          # redefine atom
                          for atom in cv.atom:
                              atom_list = model.select_atom(atom.val)
                              new_atom.append(atom_list)
                          cv["atom"] = new_atom
                      # now generate the m-expression
                      mexpr=parse_meta(meta,model)._getMExpr(CmsModel(model))
                      #print(sea.Map(generate_meta_cfg(meta, model)))
                      return mexpr

def replace_meta_with_mexpression(mexpr,input_msj,output_msj,mexpr_file):
    parsed_file=cmj.parse_msj(input_msj)
    dname=path.dirname(path.abspath(input_msj))
    newmsj=path.join(dname,output_msj)
    newmexpr=path.join(dname,mexpr_file)
    # get the abs path of input file
    for i,stg in enumerate(parsed_file): 
         print("Stage ",i,stg.NAME)

         if hasattr(stg,'param'): 
           if 'meta'  in stg.param.keys():
                  if hasattr(stg.param.meta,'cv'):
                     print("This stage has metadynamics!")
                            
                     stg.param["meta"]=sea.Atom() 
                     stg.param.meta.val="FILE"
                     stg.param.meta.reset_tag("setbyuser", propagate=True) 

                     stg.param["meta_file"]= newmexpr 
                     stg.param.meta_file.reset_tag("setbyuser", propagate=True) 

    cmj.write_msj(parsed_file,fname=newmsj)
    print("File written ",newmsj)
    with open(newmexpr,"w") as fh:
         fh.write(mexpr)
    print("File written ",newmexpr)


if __name__ == "__main__":
   parser = argparse.ArgumentParser()
   parser.add_argument('msj' , type=str,help='the path to input msj')
   parser.add_argument('cms', type=str,help='the path to input cms')
   parser.add_argument('outmsj', type=str,help='the name of output msj (will be placed in the same folder of the original msj)')
   parser.add_argument('outmexpr', type=str,help='the name output msj (will be placed in the same folder of the original msj)')
   args = parser.parse_args()
   print("Input msj ",args.msj)
   print("Input cms ",args.cms)
   print("Output msj ",args.outmsj)
   print("Output mexpression ",args.outmexpr)

   mexpr=convert_meta_into_mexpression(args.msj,args.cms)
   replace_meta_with_mexpression(mexpr,args.msj,args.outmsj,args.outmexpr)
