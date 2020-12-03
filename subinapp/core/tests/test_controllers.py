import os

import inapppy

from subinapp.core.controllers import SubscriptionsBasicController
from subinapp.core.providers.google import Verifier as GVerifier
from subinapp.interface.entities import SubscriptionManagerConfig, AppleVerifierConfig, GoogleVerifierConfig, \
    AppleExtraArgs

FAKE_APPLE_CONFIG = AppleVerifierConfig(bundle_id='com.company.myapp',
                                        extra=AppleExtraArgs(shared_secret='4rjFaspQ3419S9vXx'))
FAKE_GOOGLE_CONFIG = GoogleVerifierConfig(bundle_id='com.company.myapp',
                                          private_key_path=os.path.join(__file__, '..', 'keyfile.json'))


class GooglePlayVerifierMock(inapppy.GooglePlayVerifier):
    def __init__(self, bundle_id: str = 'some.bundle.id', private_key_path: str = '/some/file/path/file.json',
                 http_timeout: int = 15):
        ...

    def _authorize(self):
        return None


def test_base_controller_configuration():
    GVerifier.verifier_class = GooglePlayVerifierMock
    config = SubscriptionManagerConfig(apple=FAKE_APPLE_CONFIG,
                                       google=FAKE_GOOGLE_CONFIG)
    assert SubscriptionsBasicController.verifiers is None
    assert SubscriptionsBasicController.parsers is None
    assert SubscriptionsBasicController.providers is None
    SubscriptionsBasicController.configure(config)
    assert SubscriptionsBasicController.providers == {'apple', 'google'}
    assert (SubscriptionsBasicController.verifiers
            and SubscriptionsBasicController.verifiers.google
            and SubscriptionsBasicController.verifiers.apple)
    assert (SubscriptionsBasicController.parsers
            and SubscriptionsBasicController.parsers.google
            and SubscriptionsBasicController.parsers.apple)
