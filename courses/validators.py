from rest_framework import validators


class YoutubeLinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        link = value.get(self.field)
        if link and ("www.youtube.com" not in link):
            raise validators.ValidationError("You cannot add links to sources other than Youtube")
