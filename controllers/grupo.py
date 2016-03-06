# -*- coding: utf-8 -*-


@auth.requires_login()
def index():

    list_str = """ 
        <tr class="odd gradeX">
            <td>%(nome)s</td>
            <td>%(desc)s</td>
            <td><a href="%(edt)s" class="btn btn-primary btn-xs fa fa-pencil" >

                </a>
                <a href="%(delt)s" class="btn btn-primary btn-xs fa fa-trash-o" >

                </a>

            </td>

        </tr>
    """
    resp = db(Grupo).select(orderby=~Grupo.id)
    lista = [list_str % dict(nome=linha.nome,\
                             desc=linha.desc,\
                             edt=URL('grupo', 'editar', args=linha.id),\
                             delt=URL('grupo', 'desativar'),\
                             )for linha in resp]
    return dict(lista=lista)


@auth.requires_login()
def adicionar():
    form = SQLFORM(Grupo, formstyle='divs')
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
        record = Grupo(request.args(0)) or redirect(URL('index'))
        form = SQLFORM(Grupo, record, formstyle='divs')
    if form.process().accepted:
        redirect(URL('index'))
        response.flash = 'Sucesso!'
    elif form.errors:
        response.flash = 'Erros!'
    else:
        response.flash = 'Preencha os dados'
    response.view = 'grupo/adicionar.html'
    return dict(form=form)
