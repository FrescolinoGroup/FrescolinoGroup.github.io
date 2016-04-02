#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    30.03.2016 11:25:17 CEST
# File:    generate_index.py

import os
import glob
from xml.etree import ElementTree as xml


def prettify(node, indent = "    ", level = 0):
    node.tail = "\n" + indent * level
    if len(node) != 0:
        node.text = "\n" + indent * (level + 1)
        for c in node:
            prettify(c, indent, level + 1)
            if c == node[-1]:
                c.tail = "\n" + indent * level
    else:
        if node.text:
            node.text = node.text.strip()
        node.tail = "\n" + indent * level

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
    reserved_names = ['static']
    for mod_name in listdir_only_dir(path):
        if mod_name in reserved_names:
            continue
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
    
    #------------------- write html -------------------
    
    body = xml.Element("body")

    header = xml.Element("header")
    container = xml.Element("div", **{"class": "head_container"})
    figure = xml.Element("figure", **{"class": "logo"})
    figure.append(xml.Element("img", **{'src': 'static/frescolino_logo.png'}))
    container.append(figure)
    title = xml.Element("h1")
    title.text = "The Frescolino project"
    container.append(title)
    subtitle = xml.Element("h2")
    subtitle.text = "Choose a Module below"
    container.append(subtitle)
    header.append(container)
    body.append(header)

    mod_container = xml.Element("div", **{"class": "mod_container"})
    
    for M in mods:
        mod = xml.Element("div", **{"class": "module"})
        
        name = xml.Element("a", name="title")
        name.text = M["name"]
        descr = xml.Element("a", name="descr")
        descr.text = M["description"]
        
        title = xml.Element("div")
        title.append(name)
        title.append(descr)
        
        mod.append(title)
        
        versions = xml.Element("div", name="versions")
        
        default_doc = M["dev_version_path"]+"/index.html"
        lv = xml.Element("a", href=default_doc, name="latest")
        lv.text = "Latest Version {}".format(M["dev_version"])
        
        avers = xml.Element("a")
        avers.text = "All Versions"
        
        sel = xml.Element("select")
        for v, vp in zip(M["versions"], M["versions_path"]):
            attr = dict(onclick="window.location.href=\'{}/index.html\'".format(vp))
            status = ""
            if v == M["dev_version"]:
                status = "(default)"
                attr["selected"]="selected"
            elif v > M["dev_version"]:
                status = "(dev)"
            opt = xml.Element("option", **attr)
            opt.text = "{} {}".format(v, status)
            sel.append(opt)
        
        av = xml.Element("div")
        av.append(avers)
        av.append(sel)
        
        
        versions.append(lv)
        versions.append(av)
        mod.append(versions)
        mod_container.append(mod)

    body.append(mod_container)
    
    
    head = xml.Element("head")
    link = xml.Element("link", href="theme.css", rel="stylesheet", type="text/css")
    head.append(link)
    
    root = xml.Element("html")
    root.append(head)
    root.append(body)
    
    prettify(root)
    
    tree = xml.ElementTree(root)
    tree.write("index.html", method = "html")
    
if __name__ == "__main__":
    main()
