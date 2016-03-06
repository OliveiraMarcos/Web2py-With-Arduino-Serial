# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('Lamp'),XML('<i class="fa fa-lightbulb-o"></i>'),
                  _class="navbar-brand",_href="http://www.web2py.com/",
                  _id="web2py-logo")
response.title = request.application.replace('_',' ').title()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################



DEVELOPMENT_MENU = True

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

def _():
    # shortcuts
    app = request.application
    ctr = request.controller
    # useful links to internal and external resources
    response.menu = UL(
                      LI(A(I( _class='fa fa-home'),T(' Principal'), _class='active', _href=URL('default','index'))),
                      LI(
                          A(I( _class='fa fa-database'), T(' Cadastro'), SPAN( _class='caret'), data={'toggle':'dropdown'}, aria={'haspopup':'true','expanded':'false'}, _class='dropdown-toggle', _role='button'),
                          UL( 
                            LI(A(I( _class="fa fa-users"), T(' Usuario'),  _href=URL('usuario','index'))),
                            LI(A(I( _class="fa fa-key"), T(' Papel'), _href=URL('papel','index'))),
                            LI( _role="separator", _class="divider"),
                            LI(A(I( _class="fa fa-building"), T(' Dispositivo'), _href=URL('dispositivo','index'))),
                            LI(A(I( _class="fa fa-sitemap"), T(' Grupos'), _href=URL('grupo','index'))),
                            LI(A(I( _class="fa fa-info"), T(' Incons'), _href=URL('icons','index'))),
                            _class="dropdown-menu"
                          ),
                          _class='dropdown'
                      ),
                      LI(A(I( _class="fa fa-cogs"), T(' Configurações'), _href=URL('serial','index'))),
                      LI(A(I( _class="fa fa-power-off"), T(' Sair'), _href="#")),
                      _class='nav navbar-nav'
                    )
if DEVELOPMENT_MENU: _()

if "auth" in locals(): auth.wikimenu()
