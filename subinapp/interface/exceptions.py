"""
Description of exceptions that can be thrown during subscription verification
"""


class ConfigurationIsMissing(BaseException):
    """No configuration given to setup verification process"""


class VerificationFailed(BaseException):
    """Provided receipt wasn't verified, so it's bad or something wrong with settings"""