# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
#########################################################################
from gluon.contrib.websocket_messaging import websocket_send
import hashlib

@auth.requires_login()
def index():
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
    resp = db(Embarcado.id_icon == Icons.id).select(orderby=~Embarcado.id)
    lista = [room % dict(label=linha.embarcado.descricao,
                             nome=linha.embarcado.nome,
                             icon=linha.icons.icon,
                             st=status_device(linha.embarcado.status),
                             id=linha.embarcado.id,
                             clas=troggle_class(linha.embarcado.status),
                             )for linha in resp]
    return dict(lista=lista)

#websocket_messaging
#websocket_send
#from gluon.contrib.websocket_messaging import websocket_send
def devices():
    try:
        cmd = request.vars.value
        if cmd:
            res = cmd.split('-')
            row = db(Embarcado.id==res[1]).select().first()
            row2 = db(Serial.id==row.id_serial).select().first()
            if row2.status:
                rq = str(row.codigo_arduino)
                print type(rq)
                resp = device_send(row2, rq)
                row.update_record(status = not row.status)
                js = "#"+cmd
                websocket_send('http://127.0.0.1:8888',js, 'mykey', 'mygroup')
        return dict(cmd=resp)
    except Exception, e:
        return dict(cmd=e)
        pass


def section():
    import serial
    import time
    cmd = request.vars.ref
    if cmd:
        serialport = serial.Serial("COM3", 9600, timeout=0.5)
        serialport.write(cmd)
        rep = serialport.readlines(1)
        time.sleep(1)
    refIcon = _getOFF()
    refSt = 'Desligado'
    if cmd == '1':
        refIcon = _getON()
        refSt = 'Ligado'
    response.flash = 'Bem Vindo!'
    return dict(refIcon=refIcon, refSt=refSt)


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
