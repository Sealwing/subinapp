"""
Providers for different services
Settings management
"""
from typing import Optional

from subinapp.interface.entities import SubscriptionManagerConfig
from subinapp.interface.exceptions import ConfigurationIsMissing


class ControllerProvider:
    """
    Constructs and provides SubscriptionsController class
        for Subscriptions management
    """
    config: Optional[SubscriptionManagerConfig] = None

    @staticmethod
    def check_settings_presence(provider: str):
        if ControllerProvider.config is None or getattr(ControllerProvider.config, provider) is None:
            raise ConfigurationIsMissing('No configuration found for provider: %s', provider)
