from . import selectors


def perfil_empresa(request):
    return {"perfil_footer": selectors.perfil_empresa()}
