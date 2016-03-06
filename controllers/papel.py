# -*- coding: utf-8 -*-


@auth.requires_login()
def index():

    list_str = """ 
        <tr class="odd gradeX">
            <td>%(nome)s</td>
            <td>%(papel)s</td>
            <td><a href="%(edt)s" class="btn btn-primary btn-xs fa fa-pencil" >

                </a>
                <a href="%(delt)s" class="btn btn-primary btn-xs fa fa-trash-o" >

                </a>

            </td>

        </tr>
    """
    resp = db().select(
    	db.auth_membership.ALL, db.auth_user.ALL, db.auth_group.ALL,\
    	join=[db.auth_membership.on(db.auth_user.id==db.auth_membership.user_id ).
    		db.auth_membership.on(db.auth_group.id==db.auth_membership.group_id)])
    lista = [list_str % dict(nome=linha.auth_user.first_name,
                             papel=linha.auth_group.role,
                             edt=URL('papel', 'editar', args=linha.auth_membership.id),
                             delt=URL('papel', 'desativar'),
                             )for linha in resp]
    return dict(lista=lista)


@auth.requires_login()
def adicionar():
    form = SQLFORM(db.auth_membership, formstyle='divs')
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
        record = db.auth_membership(request.args(0)) or redirect(URL('index'))
        form = SQLFORM(db.auth_membership, record, formstyle='divs')
    if form.process().accepted:
        redirect(URL('index'))
        response.flash = 'Sucesso!'
    elif form.errors:
        response.flash = 'Erros!'
    else:
        response.flash = 'Preencha os dados'
    response.view = 'papel/adicionar.html'
    return dict(form=form)
