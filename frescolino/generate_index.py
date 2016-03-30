#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    30.03.2016 11:25:17 CEST
# File:    generate_index.py

import os
import glob

def listdir_only_dir(path):
    path_name = os.listdir(path)
    dirs = []
    
    for p in path_name:
        if os.path.isdir(os.path.join(path, p)):
            dirs.append(p)
    
    return dirs

def main():
    path = os.path.dirname(os.path.abspath(__file__))
    
    mod_names = sorted(listdir_only_dir(path))
    
    mods = []
    for mod_name in listdir_only_dir(path):
        print("Processing module {}".format(mod_name))
        M = dict()
        # get all versions
        M["name"] = mod_name
        M["path"] = os.path.join(path, mod_name)
        M["versions"] = list(reversed(sorted(listdir_only_dir(M["path"]))))
        M["versions_path"] = [os.path.join(mod_name, v) for v in M["versions"]]
        
        print("versions found:  {}".format(", ".join(M["versions"])))
        
        # get default version
        dev_vers = M["versions"][0] # choose latest as default
        
        dvf = os.path.join(path, mod_name, "default_version.txt")
        if os.path.isfile(dvf): # unless specified explicitly
            with open(dvf, "r") as f:
                dev_vers = f.readline().strip()
        print("default version: {}".format(dev_vers))
            
        M["dev_version"] = dev_vers
        M["dev_version_path"] = os.path.join(mod_name, dev_vers)
        
        # get description
        descr = os.path.join(path, "..", "..", "modules", mod_name, "doc", "description.txt")
        
        if not os.path.isfile(descr):
            raise RuntimeError("Module {} has no doc/describtion.txt file".format(mod_name))
        
        with open(descr, "r") as f:
            M["description"] = f.readline().strip()
        mods.append(M)
        
        print()
    
    #~ print(mods)
    #~ return 
    with open("index.html", "w") as o:
        
        o.write("<div>\n")
        
        for M in mods:
        
            o.write("<div>\n")
            o.write("<div>{} ({})</div>\n".format(M["name"], M["description"]))
            
            o.write("<div>\n")
            
            o.write('<a href="{}/index.html">Latest Version {}</a>\n'.format(M["dev_version_path"], M["dev_version"]))
            
            o.write('<a>All Versions </a>\n')
            o.write('<select>\n')
            
            for v, vp in zip(M["versions"], M["versions_path"]):
                status = ""
                sel = ""
                if v == M["dev_version"]:
                    status = "(default)"
                    sel = 'selected="selected"'
                elif v > M["dev_version"]:
                    status = "(dev)"
                
                o.write('<option {} onclick="window.location.href=\'{}/index.html\'">{} {}</option>\n'.format(sel, vp, v, status))
            
            o.write('</select>\n')
            
            o.write("</div>\n")
            o.write("</div>\n")
            
        o.write("</div>\n")
        
    
    
if __name__ == "__main__":
    main()
