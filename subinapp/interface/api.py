"""
Description of API level classes
"""
from abc import ABC, abstractmethod
from datetime import datetime

from subinapp.interface.entities import VerifiedSubscriptionInfo


class BaseVerifier(ABC):
    """Verifies receipt"""

    verifier = None

    @abstractmethod
    def verify(self, receipt: str) -> dict:
        """
        Main method to call
        It tries to verify given receipt (or one set in constructor)
        Then detects expiration date
        Then detects product id
        :raises VerificationFailed: Receipt is not valid
        :param receipt: Receipt from device
        :return: Raw dict from provider's response
        """


class BaseParser(ABC):
    """Parse response from provider"""

    def parse(self, provider_response: dict) -> VerifiedSubscriptionInfo:
        """
        Parses raw dict from provider's response
        :param provider_response: Response from provider as dict
        :return: VerifiedSubscriptionInfo with main info about subscription
        """
        return VerifiedSubscriptionInfo(
            product_id=self.detect_product_id(provider_response),
            purchase_token=self.detect_purchase_token(provider_response),
            expiration_date=self.detect_expiration_date(provider_response),
            is_renewable=self.detect_is_renewable(provider_response),
        )

    @abstractmethod
    def detect_expiration_date(self, provider_response: dict) -> datetime:
        """Get subscription expiration date"""
        ...

    @abstractmethod
    def detect_product_id(self, provider_response: dict) -> str:
        """Get subscription product_id"""
        ...

    @abstractmethod
    def detect_is_renewable(self, provider_response: dict) -> bool:
        """Get renewable status of subscription"""
        ...

    @abstractmethod
    def detect_purchase_token(self, provider_response: dict) -> str:
        """Get purchase token as unique identifier of subscription"""
        ...
