import shutil
import os
import sys
from textnode import TextNode,TextType
from builderfuncs import build_public,generate_pages_recursive

static_path = "./static"
source_path = "./content"
public_path = "./docs"
template_path = "./template.html"

def main():
    
    build_public(static_path,public_path)
    
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    spath = os.path.abspath(source_path)
    tpath = os.path.abspath(template_path)
    dpath = os.path.abspath(public_path)
    generate_pages_recursive(spath,tpath,dpath,basepath)


main()