# -*- coding: utf-8 -*-


@auth.requires_login()
def index():

    list_str = """ 
        <tr class="odd gradeX">
            <td>%(nome)s</td>
            <td>%(email)s</td>
            <td><a href="%(edt)s" class="btn btn-primary btn-xs fa fa-pencil" >

                </a>
                <a href="%(delt)s" class="btn btn-primary btn-xs fa fa-trash-o" >

                </a>

            </td>

        </tr>
    """
    resp = db(db.auth_user).select(orderby=~db.auth_user.id)
    lista = [list_str % dict(nome=linha.first_name,
                             email=linha.email,
                             edt=URL('usuario', 'editar', args=linha.id),
                             delt=URL('usuario', 'desativar'),
                             )for linha in resp]
    return dict(lista=lista)


@auth.requires_login()
def adicionar():
    form = SQLFORM(db.auth_user, formstyle='divs')
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
        record = db.auth_user(request.args(0)) or redirect(URL('index'))
        form = SQLFORM(db.auth_user, record, formstyle='divs')
    if form.process().accepted:
        redirect(URL('index'))
        response.flash = 'Sucesso!'
    elif form.errors:
        response.flash = 'Erros!'
    else:
        response.flash = 'Preencha os dados'
    response.view = 'usuario/adicionar.html'
    return dict(form=form)
