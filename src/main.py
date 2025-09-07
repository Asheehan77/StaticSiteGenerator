import shutil
import os
from textnode import TextNode,TextType
from builderfuncs import build_public,generate_pages_recursive


source_path = "content"
template_path = "template.html"
dest_path = "public"

def main():
    build_public()
    
    spath = os.path.abspath(source_path)
    tpath = os.path.abspath(template_path)
    dpath = os.path.abspath(dest_path)
    generate_pages_recursive(spath,tpath,dpath)


main()