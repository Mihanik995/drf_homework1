from rest_framework import validators


class YoutubeLinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if "www.youtube.com" not in value.get(self.field):
            raise validators.ValidationError("You cannot add links to sources other than Youtube")
