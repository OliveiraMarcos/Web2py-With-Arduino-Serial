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
                             delt=URL('usuario', 'deletar', args=linha.id),
                             )for linha in resp]
    return dict(lista=lista)


@auth.requires_login()
def adicionar():
    form = SQLFORM(db.auth_user, formstyle='divs')
    if form.process().accepted:
        response.flash = 'Sucesso!'
        redirect(URL('usuario', 'index'))
    elif form.errors:
        response.flash = 'Erros!'
    else:
        response.flash = 'Preencha os dados'
    return dict(form=form)


@auth.requires_login()
def editar():
    try:
        if request.args(0):
            user_id = request.args(0)
            if auth.user_id != int(user_id):
                response.view = 'error.html'
                return dict(msg='Você não tem permissão para alterar esse cadastro!')
            record = db.auth_user(user_id) or redirect(URL('index'))
            form = SQLFORM(db.auth_user, record, formstyle='divs')
        if form.process().accepted:
            redirect(URL('usuario', 'index'))
            response.flash = 'Sucesso!'
        elif form.errors:
            response.flash = 'Erros!'
        else:
            response.flash = 'Preencha os dados'
        response.view = 'usuario/adicionar.html'
        return dict(form=form)
    except Exception, e:
        response.view = 'error.html'
        return dict(msg=e)
        pass


@auth.requires_membership('ADM')
def deletar():
    try:
        if db(db.auth_user.id == request.args(0)).delete():
            redirect(URL('index'))
            response.flash = T('Registro Excluido com sucesso!')
        else:
            response.flash = T('Erro!')
    except Exception, e:
        response.flash = e
        pass
    redirect(URL('usuario', 'index'))
