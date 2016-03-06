# -*- coding: utf-8 -*-
import time
import serial

SERIAIS = dict()

if not request.env.web2py_runtime_gae:
    db = DAL("sqlite://storage.sqlite")
else:
    db = DAL("google:datastore+ndb")
    session.connect(request, response, db=db)
response.generic_patterns = ['*'] if request.is_local else []

from gluon.tools import Auth, Service, PluginManager
auth = Auth(db)
service = Service()
plugins = PluginManager()
# create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)


Serial = db.define_table("serial",
		Field("device", "string", length=11, requires=IS_NOT_EMPTY(), notnull=True, unique=True),
		Field("baud_rate", "integer", length=11, label="Baud Rate", comment=None, default=9600),
		Field("timeout", "integer", length=11, label="Timeout", comment=None, default=1),
		Field("parity", "string", length=1, label="Parity", comment=None, default="N"),
		Field("stopbits", "integer", length=11, label="Stopbits", comment=None, default=1),
		Field("bytesize", "integer", length=11, label="Bytesize", comment=None, default=8),
		Field("status", "boolean", label="Status", comment=None),
		auth.signature,
		format='%(device)s'
		
	)
Serial.is_active.readable = False
Serial.is_active.writable = False

Grupo = db.define_table("grupo",
		Field("nome", "string", label="Nome", length=50, requires=IS_NOT_EMPTY(), notnull=True),
		Field("desc", "string", length=80, label="Descrição", comment=None),
		auth.signature,
		format='%(nome)s'
	)
Grupo.is_active.readable = False
Grupo.is_active.writable = False

Icons = db.define_table("icons",
		Field("nome", "string", length=60, label="Nome", requires=IS_NOT_EMPTY(), notnull=True),
		Field("icon", "string", length=80, label="Icon", comment=None),
		auth.signature,
		format='%(nome)s'
	)
Icons.is_active.readable = False
Icons.is_active.writable = False


Embarcado = db.define_table("embarcado",
		Field("id_serial",Serial, label="Serial", requires=IS_NOT_EMPTY(), notnull=True),
		Field("id_grupo",Grupo , label="Grupo", requires=IS_NOT_EMPTY(), notnull=True),
		Field("id_icon",Icons , label="Icons", requires=IS_NOT_EMPTY(), notnull=True),
		Field("nome", "string", length=80, label="Nome", comment=None),
		Field("descricao", "string", length=80, label="Descrição", comment=None),
		Field("codigo_arduino", "integer", length=11, label="Arduino Cod.", comment=None),
		Field("status", "boolean", label="Status", comment=None),
		auth.signature
	)
Embarcado.is_active.readable = False
Embarcado.is_active.writable = False
Embarcado.id_serial.requires = IS_IN_DB(db, Serial.id, Serial._format)
Embarcado.id_grupo.requires = IS_IN_DB(db, Grupo.id, Grupo._format)
Embarcado.id_icon.requires = IS_IN_DB(db, Icons.id, Icons._format)



# for row in db((Serial.id > 0) & (Serial.status == True)).select():
# 	if SERIAIS:
# 		SERIAIS[row.device].close()
# 	SERIAIS[row.device] = serial.Serial(
# 		row.device,
# 		int(row.baud_rate),
# 		timeout=int(row.timeout),
# 		bytesize=int(row.bytesize),
# 		stopbits=int(row.stopbits),
# 		parity=row.parity
# 	)


def status_device(st):
	if st:
		return 'Ligado <i class="fa fa-toggle-on"></i>'
	else:
		return 'Desligado <i class="fa fa-toggle-off"></i>'

def device_send(row, msg):
	try:
		conn_serial = serial.Serial(
			row.device,
			int(row.baud_rate),
			timeout=int(row.timeout),
			bytesize=int(row.bytesize),
			stopbits=int(row.stopbits),
			parity=row.parity
		)
		conn_serial.write(msg)
		retorno = conn_serial.readline().rstrip()
		return retorno

	finally:
		conn_serial.close()
		pass