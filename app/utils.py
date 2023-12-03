import string
import random


def generate_shortcode(length: int = 6) -> str:
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))
