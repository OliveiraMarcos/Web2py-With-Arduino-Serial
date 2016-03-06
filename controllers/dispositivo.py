# -*- coding: utf-8 -*-


@auth.requires_login()
def index():

    list_str = """ 
        <tr class="odd gradeX">
            <td>%(nome)s</td>
            <td>%(serial)s</td>
            <td>%(status)s</td>
            <td><a href="%(edt)s" class="btn btn-primary btn-xs fa fa-pencil" >

                </a>
                <a href="%(delt)s" class="btn btn-primary btn-xs fa fa-trash-o" >

                </a>

            </td>
        </tr>
    """
    resp = db(Embarcado.id_serial==Serial.id).select(orderby=~Embarcado.id)
    lista = [list_str % dict(nome=linha.embarcado.nome,
                             serial=linha.serial.device,
                             status=status_device(linha.embarcado.status),
                             edt=URL('dispositivo', 'editar', args=linha.embarcado.id),
                             delt=URL('dispositivo', 'desativar'),
                             )for linha in resp]
    return dict(lista=lista)


@auth.requires_login()
def adicionar():
    form = SQLFORM(Embarcado, formstyle='divs')
    if form.process().accepted:
        response.flash = 'Sucesso!'
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'Erros!'
    else:
        response.flash = 'Preencha os dados'
    return dict(form=form)


@auth.requires_login()
def editar():
    if request.args(0):
        record = Embarcado(request.args(0)) or redirect(URL('index'))
        form = SQLFORM(Embarcado, record, formstyle='divs')
    if form.process().accepted:
        redirect(URL('index'))
        response.flash = 'Sucesso!'
    elif form.errors:
        response.flash = 'Erros!'
    else:
        response.flash = 'Preencha os dados'
    response.view = 'dispositivo/adicionar.html'
    return dict(form=form)
