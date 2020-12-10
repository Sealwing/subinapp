# subinapp

Backend verification of In App Subscriptions

## About

`subinapp` is a Python package to provide useful helper classes
for verification of subscriptions as type of IAP (In App Purchases)
and retrieving most important data for using it further in the application.

Verification process itself is based on [`inapppy` package](https://github.com/dotpot/InAppPy/).

**Available providers of IAP**
- Google (Google Play)
- Apple (App Store)

## Configuration

There are some secrets that are required for verifying receipts
both from Google and Apple.

The container classes for them are placed in `subinapp.interface.entities`.
For Google it is `GoogleVerifierConfig` and for Apple it is `AppleVerifierConfig`
with extra class `AppleExtraArgs` (is used for configuring requests).

> Both classes are properties of `SubscriptionManagerConfig`
> and if you want to initialize only on provider, set another to `None`

##### Google settings
- `bundle_id` - is the name of Android package (e.g. com.subinapp.app)
- `private_key_path` - is the path to json service key that you should get
    in Google Play console by creating service account
    with rights to check your financial operations or something like that
    
##### Apple settings
- `bundle_id` - is the same as in case with Android bundle id
- `auto_retry_wrong_env_request` - option that makes `inapppy`
    to request another environment (Sandbox or Production)
    if verification on another failed
- `sandbox` - option to check sandbox environment first or not
- `extra` - is extra options that are not used during verifier initialization
  - `shared_secret` - generally you'll need it for subscriptions
                    (if you have auto-renewable ones, as I understand),
                    so you can generate it for all your subscriptions (it is short string)
  - `exclude_old_transactions` - option for reducing size of Apple response by excluding some of operations,
                    but there still be story of IAP in `inapp` field of validation response

## Code Structure

At the time there are two main blocks: `core` and `interface`.

`interface` is about describing how to use this package, so it contains
- `api` for describing main action classes for verification and parsing of a receipt.
        Each provider has all of classes placed in here implemented.
- `entities` contains dataclasses for communication with API from inside and outside.
        Settings classes is also placed here.
- `exceptions` file has common exceptions that could occur during verification
        and are specific for this package exactly.
- `utils` for now contains only a decorator for handling parsing exceptions

`core` has the implementation of `api.BaseVerifier` and `api.BaseParser` classes in `providers` directory

> **!Note** that both classes should be implemented
> and the file in `providers` should be named after provider's settings property in `SubscriptionManagerConfig`

`core.controllers` provides a high level API for verification and validation
that could be used as base for use as a controller at API Endpoint.

```python
# basic usage of controller

from subinapp.core.controllers import SubscriptionsBasicController
from subinapp.interface.entities import SubscriptionManagerConfig, ProcessedReceipt

# get settings from your settings manager and set it instead of None
providers_settings = SubscriptionManagerConfig(apple=None, google=None)

SubscriptionsBasicController.configure(config=providers_settings)

# then handle some HTTP call on your endpoint
# smt like
# @app.post('api/awesome/endpoint/')
def register_receipt(request):
    receipt = request.get('receipt')
    provider = request.get('provider')
    if receipt and provider:
        result: ProcessedReceipt = SubscriptionsBasicController.verify_receipt(receipt=receipt, provider=provider)
        # here better to validate receipt as unused
        # and then you can save it in your db
```

For **tests** use `pytest`.

Unfortunately it's difficult to test full cycle from getting real receipt
to get parsed version of it, so tests is currently written for checking basic concepts of `subinapp`.
