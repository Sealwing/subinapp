"""
Controllers to use from application
"""

import dataclasses
import json
import logging
from collections import namedtuple
from importlib import import_module
from typing import Optional

from subinapp.interface.api import BaseVerifier, BaseParser
from subinapp.interface.entities import SubscriptionManagerConfig, ProcessedReceipt, VerifiedSubscriptionInfo
from subinapp.interface.exceptions import ConfigurationIsMissing, UndefinedProvider

log = logging.getLogger(__name__)


class SubscriptionsBasicController:
    """
    Configuration of validators and parsers for providers
    API for basic actions with receipt verification
    """
    config: Optional[SubscriptionManagerConfig] = None
    providers: Optional[set] = None
    verifiers = None
    parsers = None

    @classmethod
    def configure(cls, config: SubscriptionManagerConfig):
        """
        Gets providers to be configured from not None config field names
        Sets validators and parsers for each provider as class properties
        Validator and Parser is taken from subinapp.core
        """
        cls.config = config
        providers = {k for k, v in dataclasses.asdict(config).items() if v}
        if len(providers) == 0:
            raise ConfigurationIsMissing('No provider configurations found')
        cls.providers = providers
        log.info('Configuring validators and parsers for providers: %s', ', '.join(cls.providers))
        provider_modules = {p: import_module('subinapp.core.providers.{}'.format(p)) for p in cls.providers}
        # Prepare namedtuple class instances
        ProviderVerifiers = namedtuple('ProviderVerifiers', cls.providers)
        ProviderParsers = namedtuple('ProviderParsers', cls.providers)
        cls.verifiers = ProviderVerifiers(**{p: provider_modules[p].Verifier(cls.config) for p in cls.providers})
        cls.parsers = ProviderParsers(**{p: provider_modules[p].Parser() for p in cls.providers})

    @classmethod
    def verify_receipt(cls, provider: str, receipt: str) -> ProcessedReceipt:
        """
        Returns verified and parsed receipt or raises exception from verifier or parser
        :param provider: Provider title in lowercase
        :param receipt: In app purchase receipt from device
        """
        cls._is_provider_in_list(provider)
        verifier: BaseVerifier = getattr(cls.verifiers, provider)
        provider_response: dict = verifier.verify(receipt)
        parser: BaseParser = getattr(cls.parsers, provider)
        subscription_info: VerifiedSubscriptionInfo = parser.parse(provider_response)
        return ProcessedReceipt(provider=provider,
                                subscription_info=subscription_info,
                                receipt=json.dumps(receipt).encode('utf-8'),
                                provider_response=json.dumps(provider_response).encode('utf-8'))

    @classmethod
    def _is_provider_in_list(cls, provider: str):
        """
        Checks if provider in cls.parsers
        :raises UndefinedProvider: If provider not in cls.providers
        """
        if provider not in cls.parsers:
            raise UndefinedProvider('Provider %s is not configured for class %s', provider, cls.__name__)
