from utils import get_random_string_and_numbers




def generate_random_token(instance, size=50, token=None):
    klass = instance.__class__
    if token is None:
        new_token = get_random_string_and_numbers(size=size)
    else:
        new_token = token

    if klass.objects.filter(auth_token=new_token).exists():
        tkn = get_random_string_and_numbers(size=size)
        return generate_random_token(instance, size=size, token=tkn)
    else:
        return new_token
