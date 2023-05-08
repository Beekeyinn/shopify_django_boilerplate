import random
import string


def get_random_string_and_numbers(
    chars=string.ascii_lowercase
    + string.ascii_uppercase
    + string.digits
    + "!@$%^*",
    size=50,
):
    return "".join(random.choices(chars, k=size))
