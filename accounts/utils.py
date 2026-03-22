def es_alumno(user):
    return user.groups.filter(name='Alumno').exists()

def es_profesor(user):
    return user.groups.filter(name='Profesor').exists()

def es_preceptor(user):
    return user.groups.filter(name='Preceptor').exists()

def es_director(user):
    return user.groups.filter(name='Director').exists()




def es_preceptor_o_director(user):
    return es_preceptor(user) or es_director(user)