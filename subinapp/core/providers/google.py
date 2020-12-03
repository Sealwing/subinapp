"""
Implementation of Verifier and Parser for Google Play subscriptions
"""

import json
import logging
from datetime import datetime

import inapppy

from subinapp.interface.api import BaseVerifier, BaseParser
from subinapp.interface.exceptions import VerificationFailed
from subinapp.interface.utils import parsing_exception

log = logging.getLogger(__name__)


class Verifier(BaseVerifier):
    """Google verifier based on inapppy.GooglePlayVerifier"""

    verifier_class = inapppy.GooglePlayVerifier
    provider = 'google'

    def verify(self, receipt: str) -> dict:
        decoded_receipt = json.loads(receipt)
        purchase_token = decoded_receipt['purchaseToken']
        product_sku = decoded_receipt['productId']
        try:
            result = self.verifier.verify_with_result(
                purchase_token,
                product_sku,
                is_subscription=True
            )
            # result contains data
            return result.raw_response
        except inapppy.errors.GoogleError as e:
            log.warning('Purchase validation failed: %s', e)
            log.exception(e)
            raise VerificationFailed('Verification failed due to following reason: %s', e)


class Parser(BaseParser):
    """Google receipt parser"""

    @parsing_exception('Google','expiration date')
    def detect_expiration_date(self, provider_response: dict) -> datetime:
        return datetime.fromtimestamp(int(provider_response['expiryTimeMillis'] / 1000))

    @parsing_exception('Google','product id')
    def detect_product_id(self, provider_response: dict) -> str:
        return provider_response['productId']

    @parsing_exception('Google','renewable flag')
    def detect_is_renewable(self, provider_response: dict) -> bool:
        return bool(provider_response['autoRenewing'])

    @parsing_exception('Google', 'purchase token')
    def detect_purchase_token(self, provider_response: dict) -> str:
        return provider_response['purchaseToken']
