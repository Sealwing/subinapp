import logging

from subinapp.interface.exceptions import ParsingFailed

log = logging.getLogger(__name__)


def parsing_exception(item_to_extract: str):
    """
    Decorator for try - except during receipt parsing
    Changed exception on ParsingFailed
    :param item_to_extract: Description of thing that was extracting at the time error occurred
    :raises ParsingFailed: Some exception occured during parsing of receipt
    :return:
    """

    def decorator(func):
        def proxy_exception(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log.warning('Exception during receipt parsing occurred')
                log.exception(e)
                raise ParsingFailed('Failed to extract expiration date from response due to exception: %s',
                                    item_to_extract)

        return proxy_exception

    return decorator