"""
Classes that are used in process of subscription check
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class AppleVerifierConfig:
    """
    Required fields for verification of Apple IAP

    bundle_id - Bundle ID of mobile application
        e.g. com.company.awesomapp
    shared_secret - Short string with secret to use with auto-renewable subscriptions
    auto_retry_wrong_env - Tells inapppy to retry validation on different env (Prod or Sandbox)
    sandbox - First send to sandbox
    exclude_old_transactions - Remove old transactions from validation response
    """
    bundle_id: str
    shared_secret: str
    auto_retry_wrong_env: bool = True
    sandbox: bool = False
    exclude_old_transactions: bool = True


@dataclass
class GoogleVerifierConfig:
    """
    Required fields for verification of Google IAP

    bundle_id - Bundle ID of mobile application
        e.g. com.company.awesomapp
    sa_key_file - Path to service key to check payments
    """
    bundle_id: str
    sa_key_file: str


@dataclass
class SubscriptionManagerConfig:
    """
    Configuration for all providers
    """
    apple: Optional[AppleVerifierConfig]
    google: Optional[GoogleVerifierConfig]


@dataclass
class VerifiedSubscriptionInfo:
    """
    Main subscription information

    product_id - identifier of subscription
    purchase_token - unique identifier of purchase
    expiration_date - datetime.datetime of subscription end
    """
    product_id: str
    purchase_token: str
    expiration_date: datetime
    is_renewable: bool


@dataclass
class ProcessedReceipt:
    """
    Result of receipt verification and parsing

    subscription_info - result of subscription extraction
    receipt - result of json.dumps on input receipt
    provider_response - result of json.dumps on raw response from provider
    """
    subscription_info: VerifiedSubscriptionInfo
    receipt: bytes
    provider_response: bytes
