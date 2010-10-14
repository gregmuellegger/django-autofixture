# -*- coding: utf-8 -*-
import os
from fabric.api import abort, cd, local, env, run, settings, sudo


#################
# Documentation #
#################

def packagedocs():
    builddocs('html')
    try:
        os.mkdir('dist')
    except OSError:
        pass
    with cd('docs/_build/html'):
        local('find -print | zip docs.zip -@')
    local('mv docs/_build/html/docs.zip dist')

def builddocs(output='html'):
    with cd('docs'):
        local('make %s' % output, capture=False)

def opendocs(where='index', how='default'):
    '''
    Rebuild documentation and opens it in your browser.

    Use the first argument to specify how it should be opened:

        `d` or `default`: Open in new tab or new window, using the default
        method of your browser.

        `t` or `tab`: Open documentation in new tab.

        `n`, `w` or `window`: Open documentation in new window.
    '''
    import webbrowser
    docs_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'docs')
    index = os.path.join(docs_dir, '_build/html/%s.html' % where)
    builddocs('html')
    url = 'file://%s' % os.path.abspath(index)
    if how in ('d', 'default'):
        webbrowser.open(url)
    elif how in ('t', 'tab'):
        webbrowser.open_new_tab(url)
    elif how in ('n', 'w', 'window'):
        webbrowser.open_new(url)

docs = opendocs
