from django.contrib.auth.tokens import PasswordResetTokenGenerator


class DefaultTokenGenerator(PasswordResetTokenGenerator):
    """
    Generate and check tokens.
    """


default_token_generator = DefaultTokenGenerator()
