from .utils import es_alumno, es_profesor, es_preceptor, es_director, es_preceptor_o_director

def roles(request):
    user = request.user

    return {
        'es_alumno': user.is_authenticated and es_alumno(user),
        'es_profesor': user.is_authenticated and es_profesor(user),
        'es_preceptor': user.is_authenticated and es_preceptor(user),
        'es_director': user.is_authenticated and es_director(user),
        'es_preceptor_o_director': user.is_authenticated and es_preceptor_o_director(user),
    }
