import os
import shutil
from markdown_to_html import markdown_to_html_node

def build_public(pathstat,pathpub):
    if os.path.exists(pathpub):
        shutil.rmtree(pathpub)
    os.mkdir(pathpub)
    if os.path.exists(pathstat):
        rec_build(pathstat,pathpub,os.listdir(pathstat))
    else:
        raise Exception("Static Folder Missing")
    
def rec_build(pathstat,pathpub,file_list):
    for item in file_list:
        if os.path.isdir(pathstat+"/"+item):
            recpathstat = pathstat+"/"+item
            recpathpub = pathpub+"/"+item
            os.mkdir(recpathpub)
            reclist = os.listdir(recpathstat)
            rec_build(recpathstat,recpathpub,reclist)
        else:
            shutil.copy(pathstat+"/"+item,pathpub+"/"+item)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if len(line) < 3:
            continue
        if line[0:2] == "# ":
            return line[2:]
        
    raise Exception("Header Missing")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating Page from:\n{from_path}\nto:\n{template_path}\nusing:\n{dest_path}")
    source = ""
    template = ""
    with open(from_path,'r') as file:
        source = file.read()
    with open(template_path,'r') as file:
        template = file.read()
    htmlnodes = markdown_to_html_node(source)
    title = extract_title(source)
    rawhtml = htmlnodes.to_html()
    template = template.replace("{{ Title }}",title)
    fullpage = template.replace("{{ Content }}",rawhtml)
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    with open(dest_path,"w")as file:
        file.write(fullpage)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path,base_path):
    if os.path.isdir(dir_path_content):
        for item in os.listdir(dir_path_content):
            filename = item
            if item == "index.md":
                filename = "index.html"
            fpath = dir_path_content+"/"+item
            dpath = dest_dir_path+"/"+filename
            generate_pages_recursive(fpath,template_path,dpath,base_path)
    else:
        source = ""
        template = ""
        with open(dir_path_content,'r') as file:
            source = file.read()
        with open(template_path,'r') as file:
            template = file.read()
        htmlnodes = markdown_to_html_node(source)
        title = extract_title(source)
        rawhtml = htmlnodes.to_html()
        template = template.replace("{{ Title }}",title)
        template = template.replace("{{ Content }}",rawhtml)
        template = template.replace('href="/', 'href="' + base_path)
        template = template.replace('src="/', 'src="' + base_path)

        if not os.path.exists(os.path.dirname(dest_dir_path)):
            os.makedirs(os.path.dirname(dest_dir_path))
        with open(dest_dir_path,"w")as file:
            file.write(template)