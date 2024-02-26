from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    """
    Generates token for email verification
    """

    pass


default_email_verification_token_generator = EmailVerificationTokenGenerator()
