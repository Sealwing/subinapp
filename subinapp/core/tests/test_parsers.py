from datetime import datetime, timedelta

from subinapp.core.providers.google import Parser as GParser
from subinapp.core.providers.apple import Parser as AParser
from subinapp.interface.api import BaseParser
from subinapp.interface.entities import VerifiedSubscriptionInfo
from subinapp.interface.exceptions import ParsingFailed


def test_google_parser_with_correct_data():
    timestamp = datetime.utcnow().timestamp()
    data = {
        # date in millis
        'expiryTimeMillis': timestamp * 1000,
        'productId': 'com.example.myproduct',
        'purchaseToken': 'ASlkj39fj0flkj1ljF!jf32f-sdvkljoi(A',
        'autoRenewing': True,
    }
    parser: BaseParser = GParser()
    result: VerifiedSubscriptionInfo = parser.parse(data)
    assert int(result.expiration_date.timestamp()) == int(timestamp)
    assert result.product_id == data['productId']
    assert result.purchase_token == data['purchaseToken']
    assert result.is_renewable is True


def test_google_parser_with_incorrect_data():
    parser: BaseParser = GParser()
    try:
        parser.parse({'productId': None})
    except ParsingFailed:
        pass
    else:
        # exception should be raised
        assert False


def test_apple_parser_with_correct_data():
    cur_time = int(datetime.utcnow().timestamp() * 1000)
    past_time = int((datetime.utcnow() - timedelta(days=5)).timestamp() * 1000)
    data = {
        'latest_receipt_info': [
            # check sorting to get newest subscription
            {
                'expires_date_ms': past_time,
                'product_id': 'com.product.old',
                'transaction_id': '12359344092384109945'
            },
            {
                'expires_date_ms': cur_time,
                'product_id': 'com.product.new',
                'transaction_id': '48903258904286209385'
            },
        ],
        'pending_renewal_info': [
            {
                'product_id': 'com.product.new',
                'auto_renew_status': '1'
            },
            {
                'product_id': 'com.product.old',
                'auto_renew_status': '0'
            }
        ]
    }
    parser: BaseParser = AParser()
    result: VerifiedSubscriptionInfo = parser.parse(data)
    assert result.purchase_token == '48903258904286209385'
    assert result.is_renewable is True
    assert result.product_id == 'com.product.new'
