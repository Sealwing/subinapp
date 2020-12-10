"""
Classes that are used in process of subscription check
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class AppleExtraArgs:
    """
    Extra arguments for calling verification method
    exclude_old_transactions - Remove old transactions from validation response
    shared_secret - Short string with secret to use with auto-renewable subscriptions
    """
    shared_secret: Optional[str] = None
    exclude_old_transactions: bool = True


@dataclass
class AppleVerifierConfig:
    """
    Required fields for verification of Apple IAP

    bundle_id - Bundle ID of mobile application
        e.g. com.company.awesomapp
    auto_retry_wrong_env_request - Tells inapppy to retry validation on different env (Prod or Sandbox)
    sandbox - First send to sandbox
    extra - Additional parameters for verification process, that shouldn't be provided into verifier constructor
    """

    bundle_id: str
    extra: AppleExtraArgs
    auto_retry_wrong_env_request: bool = True
    sandbox: bool = False


@dataclass
class GoogleVerifierConfig:
    """
    Required fields for verification of Google IAP

    bundle_id - Bundle ID of mobile application
        e.g. com.company.awesomapp
    private_key_path - Path to service key to check payments
    """

    bundle_id: str
    private_key_path: str


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
    is_renewable - indicator of renewable subscription
    """

    product_id: str
    purchase_token: str
    expiration_date: datetime
    is_renewable: bool


@dataclass
class ProcessedReceipt:
    """
    Result of receipt verification and parsing

    provider - provider name
    subscription_info - result of subscription extraction
    receipt - result of utf-8 encoded json.dumps on input receipt string
    provider_response - result of utf-8 encoded json.dumps on raw response from provider string
    """

    provider: str
    subscription_info: VerifiedSubscriptionInfo
    receipt: bytes
    provider_response: bytes
