# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
#########################################################################
from gluon.contrib.websocket_messaging import websocket_send


@auth.requires_login()
def index():
    room = """
    <div class="col-md-3">
        <div class="dash-unit">
            <dtitle>Dispositivos da %(desc)s</dtitle>
            <hr>
            <h2><a href="%(sec)s">%(nome)s</a></h2>
            <h3>Todos <span class="badge">%(count)s</span></h3>
            <h3>Ligados <span class="badge">%(on)s</span></h3>
            <h3>Desligados <span class="badge">%(off)s</span></h3>
            <a href="%(off_all)s">
                <div class="info-user">
                    <span aria-hidden="true" class="fa fa-power-off fs1"></span> Desligar
                </div>
            </a>
        </div>
    </div>    
    """
    resp = db(Grupo).select(orderby=~Grupo.id)
    lista = [room % dict(nome=linha.nome,
                        desc=linha.desc,
                        on=_count(linha.id, True),
                        off=_count(linha.id, False),
                        count=_count(linha.id, None),
                        sec=URL('default', 'section', args=linha.id),
                        off_all=URL('default','off_all', args=linha.id),
                        ) for linha in resp]
    return dict(lista=lista)

def _count(id,type):
    if type == None:
        return db((Embarcado.id_grupo == id) & (Embarcado.id_grupo == id)).count()
    else:
        return db((Embarcado.id_grupo == id) & (Embarcado.status == type)).count()


#websocket_messaging
#websocket_send
#from gluon.contrib.websocket_messaging import websocket_send
def devices():
    try:
        cmd = request.vars.value
        tok = request.vars.tokken
        resp = ''
        js = ''
        if cmd and tok:
            if tok == get_tokken():
                res = cmd.split('-')
                row = db((Embarcado.id==res[1])&(Embarcado.id_serial == Serial.id)).select().first()
                if row.serial.status:
                    rq = str(row.embarcado.codigo_arduino)
                    resp = int(device_send(row.serial, rq))
                    row.embarcado.update_record(status = resp)
                    js = "on_off('%s', %s)" % (cmd,resp)
                    js2 = "window.location.reload()"
                    websocket_send('http://127.0.0.1:8888',js, 'mykey', 'mysection')
                    websocket_send('http://127.0.0.1:8888',js2, 'mykey', 'mygroup')
                else:
                    resp = "%s Desativada!" % (row2.device)
            else:
                resp = "Tokken incorreto!\nAtualize sua página!"
        else:
            resp = "Parametros Vazios!"
        
        return dict(cmd=resp)
    except Exception, e:
        return dict(cmd=e)
        pass

def off_all():
    if request.args(0):
        dev = db((Embarcado.id_serial==Serial.id)
            &(Embarcado.id_grupo==request.args(0))
            &(Serial.status==True)
            &(Embarcado.status==True)
        ).select()
        for row in dev:
            if row.serial.status:
                rq = str(row.embarcado.codigo_arduino)
                resp = int(device_send(row.serial, rq))
                row.embarcado.update_record(status = resp)
        js = 'window.location.reload()'
        websocket_send('http://127.0.0.1:8888',js, 'mykey', 'mygroup')
        websocket_send('http://127.0.0.1:8888',js, 'mykey', 'mysection')
    redirect(URL('default', 'index'))

def section():
    try:
        if request.args(0):
            room = """
            <div class="col-md-3">
                <div class="lamp-unit %(clas)s" id="lamp-%(id)s" data-value="%(id)s">
                    <dtitle>%(label)s</dtitle>
                    <div class="body">
                        
                        <div class="icon-lamp fa-5x">
                            %(icon)s
                        </div>
                        <div class="h1">%(nome)s</div>
                        <div class="h3">%(st)s</div>
                    </div><!-- /thumbnail -->
                </div>
            </div>
            """
            resp = db((Embarcado.id_icon == Icons.id)&(Embarcado.id_grupo == request.args(0))).select(orderby=~Embarcado.id)
            lista = [room % dict(label=linha.embarcado.descricao,
                                     nome=linha.embarcado.nome,
                                     icon=linha.icons.icon,
                                     st=status_device(linha.embarcado.status),
                                     id=linha.embarcado.id,
                                     clas=troggle_class(linha.embarcado.status),
                                     )for linha in resp]
            return dict(lista=lista, tokken=get_tokken())
    except Exception, e:
        response.view = 'error.html'
        return dict(msg=e)
    


def troggle_class(st):
    if st:
        return 'lamp-ligado'
    else:
        return ''

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
