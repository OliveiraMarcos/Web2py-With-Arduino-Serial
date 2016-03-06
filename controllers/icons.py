# -*- coding: utf-8 -*-


@auth.requires_login()
def index():

    list_str = """ 
        <tr class="odd gradeX">
            <td>%(nome)s</td>
            <td>%(icon)s</td>
            <td><a href="%(edt)s" class="btn btn-primary btn-xs fa fa-pencil" >

                </a>
                <a href="%(delt)s" class="btn btn-primary btn-xs fa fa-trash-o" >

                </a>

            </td>

        </tr>
    """
    resp = db(Icons).select(orderby=~Icons.id)
    lista = [list_str % dict(nome=linha.nome,
                             icon=linha.icon,
                             edt=URL('icons', 'editar', args=linha.id),
                             delt=URL('icons', 'desativar'),
                             )for linha in resp]
    return dict(lista=lista)


@auth.requires_login()
def adicionar():
    form = SQLFORM(Icons, formstyle='divs')
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
        record = Icons(request.args(0)) or redirect(URL('index'))
        form = SQLFORM(Icons, record, formstyle='divs')
    if form.process().accepted:
        redirect(URL('index'))
        response.flash = 'Sucesso!'
    elif form.errors:
        response.flash = 'Erros!'
    else:
        response.flash = 'Preencha os dados'
    response.view = 'icons/adicionar.html'
    return dict(form=form)
