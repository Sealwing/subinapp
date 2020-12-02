import logging
from datetime import datetime

import inapppy

from subinapp.interface.api import BaseVerifier, BaseParser
from subinapp.interface.entities import AppleVerifierConfig, VerifiedSubscriptionInfo
from subinapp.interface.exceptions import VerificationFailed

log = logging.getLogger(__name__)


class Verifier(BaseVerifier):
    def __init__(self, config: AppleVerifierConfig):
        self.verifier = inapppy.AppStoreValidator(
            config.bundle_id,
            auto_retry_wrong_env_request=config.auto_retry_wrong_env,
            sandbox=config.sandbox
        )
        self.exclude_old_transactions = config.exclude_old_transactions
        self.shared_secret = config.shared_secret

    def verify(self, receipt: str) -> dict:
        try:
            return self.verifier.validate(receipt=receipt,
                                          shared_secret=self.shared_secret,
                                          exclude_old_transactions=self.exclude_old_transactions)
        except inapppy.InAppPyValidationError as e:
            response_from_apple = e.raw_response
            log.warning(f'Apple receipt check failed: %s', response_from_apple)
            log.exception(e)
            raise VerificationFailed('Verification failed due to following reason: %s', e)


class Parser(BaseParser):

    def parse(self, provider_response: dict) -> VerifiedSubscriptionInfo:
        # Most of main subscription info is in latest_receipt_info list
        latest_receipts_info: list = provider_response['latest_receipt_info']
        # first will be with max expires_date_ms value, so most fresh
        latest_receipts_info.sort(key=lambda x: x['expires_date_ms'], reverse=True)
        # So we need to add extra field detecting the most fresh subscription
        provider_response['last_receipt'] = latest_receipts_info[0]
        return super(Parser, self).parse(provider_response)

    def detect_expiration_date(self, provider_response: dict) -> datetime:
        return datetime.fromtimestamp(
            int(provider_response['last_receipt']['expires_date_ms']) / 1000
        )

    def detect_product_id(self, provider_response: dict) -> str:
        return provider_response['last_receipt']['product_id']

    def detect_is_renewable(self, provider_response: dict) -> bool:
        if ('pending_renewal_info' not in provider_response.keys()
                or len(provider_response['pending_renewal_info']) == 0):
            log.warning(f'Failed to detect renewable status, setting to False')
            return False
        auto_renew = [
            x for x in
            filter(lambda x: x['product_id'] == self.detect_product_id(provider_response),
                   provider_response['pending_renewal_info'])
        ]
        if len(auto_renew) == 0:
            return False
        return auto_renew[0]['auto_renew_status'] == '1'

    def detect_purchase_token(self, provider_response: dict) -> str:
        return provider_response['last_receipt']['transaction_id']
