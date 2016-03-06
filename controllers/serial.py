# -*- coding: utf-8 -*-


@auth.requires_login()
def index():

    list_str = """ 
        <tr class="odd gradeX">
            <td>%(porta)s</td>
            <td>%(velo)s</td>
            <td>%(status)s</td>
            <td><a href="%(edt)s" class="btn btn-primary btn-xs fa fa-pencil" >

                </a>
                <a href="%(delt)s" class="btn btn-primary btn-xs fa fa-trash-o" >

                </a>

            </td>

        </tr>
    """
    resp = db(Serial).select(orderby=~Serial.id)
    lista = [list_str % dict(porta=linha.device,
                             velo=linha.baud_rate,
                             status=linha.status,
                             edt=URL('serial', 'editar', args=linha.id),
                             delt=URL('serial', 'desativar'),
                             )for linha in resp]
    return dict(lista=lista)


@auth.requires_login()
def adicionar():
    form = SQLFORM(Serial, formstyle='divs')
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
        record = Serial(request.args(0)) or redirect(URL('index'))
        form = SQLFORM(Serial, record, formstyle='divs')
    if form.process().accepted:
        redirect(URL('index'))
        response.flash = 'Sucesso!'
    elif form.errors:
        response.flash = 'Erros!'
    else:
        response.flash = 'Preencha os dados'
    response.view = 'serial/adicionar.html'
    return dict(form=form)
