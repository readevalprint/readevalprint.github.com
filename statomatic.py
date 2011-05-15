'''
Run this with $ python ./statomatic.py runserver and go to http://localhost:8000/
Deploy with $ python ./statomatic.py render and rsync your files to a 
public_html folder.
'''

import os, sys, itertools
from  django.conf.urls.defaults import patterns
from django.template.response import SimpleTemplateResponse
from django.template import TemplateDoesNotExist
from django.http import Http404
from BeautifulSoup import BeautifulSoup
from markdown2 import markdown


# helper function to locate this dir
here = lambda x: os.path.join(os.path.abspath(os.path.dirname(__file__)), x)
me = os.path.splitext(os.path.split(__file__)[1])[0]

# SETTINGS
DEBUG=TEMPLATE_DEBUG=True
ROOT_URLCONF = me
DATABASES = { 'default': {} } #required regardless of actual usage
CONTENT_DIR = here('content')
TEMPLATE_DIRS = (CONTENT_DIR, here('templates'),)
DEPLOY_DIR = here('')
INSTALLED_APPS = ('django.contrib.markup',)

def smart_render(template, context={}):
    '''
    takes a path and tries to render it directly or the index file within it.
    TODO: can make pretty urls in the future by putting all files in folders and
    naming them index
    '''
    template = template.rstrip('/')
    for suffix in ['','/index.html','index.html']:
        try:
            return SimpleTemplateResponse(template+suffix, context).render()
        except TemplateDoesNotExist:
            pass
    raise Http404

def markdownify(rendered_template):
    '''
    parse a rendered temaplte for tags that have class="md" and replace the
    contents of the tag withthe marked up results.
    '''
    html = BeautifulSoup(rendered_template)
    for md in html.findAll('','md'):
        md.contents = BeautifulSoup(markdown(md.renderContents()))
    return html.renderContents() 

# VIEW
def index(request, template):
    r = smart_render(template)
    r.content  = markdownify(r.rendered_content)
    return r

# TODO: process all blog templates to pull title from them and populate the context.
def blog(request,template):
    template = 'blog/'+template.rstrip('/')
    return smart_render(template, context={'name':'bill'})

# URLS
urlpatterns = patterns('',
    # do something different with blog stuff
    #(r'^blog/(?P<template>[a-zA-Z0-9\-\.\/]*)$', blog), 
    (r'^(?P<template>[a-zA-Z0-9\-\.\/]*)$', index))


# RENDER 
def render():
    '''
    Takes everything in the CONTENT folder and renders and writes it to the
    DEPLOY folder
    '''
    from django.test.client import Client
    client = Client()
    for root, dirs, files in os.walk(CONTENT_DIR):
        for f in files:
            # ignore hidden files 
            if f[0] != '.':
                url = root.replace(CONTENT_DIR,'')+'/'+f
                response = client.get(url)
                out = os.path.join(DEPLOY_DIR,url[1:])
                d = os.path.dirname(out)
                if not os.path.exists(d):
                    os.makedirs(d)
                f = open(out, 'w')
                f.write(response.content)
                f.close()

def run():
    sys.path += (here('.'),)
    # set the ENV
    os.environ['DJANGO_SETTINGS_MODULE'] = me
 
if __name__ == '__main__':
    from django.core import management
    run()
    try:
        if sys.argv[1] == 'render':
                render()
        elif sys.argv[1] == 'runserver':
                management.call_command('runserver','0.0.0.0:8000' )
        else:
            print "please use with 'render' or 'runserver'"
    except:
        print "please use with 'render' or 'runserver'"
