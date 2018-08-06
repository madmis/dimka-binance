from binance.client import Client
from dimka.core.dto import PairInfo, BookTicker


class BinanceClient(Client):
    API_VERSION_V3 = 'v3'

    def __init__(self, api_key: str, api_secret: str, requests_params: dict = None):
        super().__init__(api_key, api_secret, requests_params)

    def get_pair_info(self, pair: str) -> PairInfo:
        return PairInfo(**self.get_symbol_info(pair))

    def get_book_ticker(self, symbol: str) -> BookTicker:
        """
        Best price/qty on the order book for a symbol.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#symbol-order-book-ticker

        :param: symbol
        :returns: BookTicker
        :raises: BinanceRequestException, BinanceAPIException

        """
        ticker = self._get('/ticker/bookTicker', False, self.API_VERSION_V3, data={"symbol": symbol})

        return BookTicker(**ticker)
