from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from random import choices, choice, shuffle


class PasswordGenerator:
    def __init__(self, length=8, uppercase=False, numbers=True, special_symbols=False):
        self.length = length
        self.uppercase = uppercase
        self.numbers = numbers
        self.special_symbols = special_symbols

    def generate(self):
        allowed_symbols = ascii_lowercase
        length = self.length
        password = []

        if self.uppercase:
            allowed_symbols += ascii_uppercase
            password += choice(ascii_uppercase)
            length -= 1
        if self.numbers:
            allowed_symbols += digits
            password += choice(digits)
            length -= 1
        if self.special_symbols:
            allowed_symbols += punctuation
            password += choice(punctuation)
            length -= 1

        password += choices(allowed_symbols, k=length)
        shuffle(password)

        return "".join(password)
