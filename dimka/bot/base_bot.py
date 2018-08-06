from argparse import Namespace
import datetime
from decimal import Decimal, ROUND_UP
from typing import Tuple, List

from dimka.core.config import Config
import dimka.core.utils as utils
import dimka.core.models as bot_models
from dimka.core.client import BinanceClient
from dimka.core.dto import Order, TradeResult, Ticker


class BaseBot(object):
    def __init__(self, client: BinanceClient, config: Config, args: Namespace):
        self.client = client
        self.params = config.params
        self.pair = config.params.get("pair")
        self.logger = config.log
        self.args = args
        self.pair_info = self.client.get_pair_info(self.pair)

    def run(self):
        raise NotImplementedError(
            "{} bot: should implement run() method.".format(
                self.params.get("bot_name")
            )
        )

    def funds(self) -> Tuple[Decimal, Decimal]:
        """
        Get account funds according to trading pair:
            base coin, quote (secondary) coin (from current pair)

        Returns:
            Tuple[Decimal, Decimal]: first - is base coin funds, second - quote coin funds
        """
        base_funds = self.client.get_asset_balance(asset=self.pair_info.baseAsset)
        if not base_funds:
            base_funds = {"free": "0"}
        quote_funds = self.client.get_asset_balance(asset=self.pair_info.quoteAsset)
        if not base_funds:
            quote_funds = {"free": "0"}

        return Decimal(base_funds["free"]), Decimal(quote_funds["free"])

    def active_orders(self, side: str = None) -> List[Order]:
        """
        Get active orders list.
        If defined side (buy, sell) return orders with this side

        :param side: BinanceClient.SIDE_BUY or BinanceClient.SIDE_SELL
        :return:
        """

        orders = self.client.get_open_orders(symbol=self.pair)

        if side is not None:
            result = []
            for order in orders:
                if order.type == side:
                    result.append(order)

            return result

        return orders

    def cancel_buy_orders(self):
        """ Cancel all opened BUY orders """
        buy_orders = self.active_orders(BinanceClient.SIDE_BUY)

        if len(buy_orders) > 0:
            self.logger.warning("Cancel all opened BUY orders: {}".format(len(buy_orders)))

            for order in buy_orders:
                result = self.client.cancel_order(symbol=self.pair, orderId=order.orderId)
                self.logger.debug("  Canceled order #{}".format(result['orderId']))

    def top_sell_price(self) -> Decimal:
        """ Top sell price - top price from sell queue """
        ticker = self.client.get_book_ticker(self.pair)

        return ticker.askPrice

    def top_buy_price(self) -> Decimal:
        """ Top buy price - top price from buy queue """
        ticker = self.client.get_book_ticker(self.pair)

        return ticker.bidPrice

    def get_price_unit(self) -> Decimal:
        """ Get minimum price unit for current pair  """
        return utils.td(utils.quanta[-1], self.pair_info.quotePrecision, ROUND_UP)

    def create_buy_order(self, buy_price: Decimal, buy_amount: Decimal) -> TradeResult:
        """ Create buy order """
        trade = self.client.order_limit_buy(
            symbol=self.pair,
            quantity=buy_amount,
            price=buy_price,
        )

        return TradeResult(**trade)

    def create_sell_order(self, sell_price: Decimal, sell_amount: Decimal) -> TradeResult:
        """ Create buy order """
        trade = self.client.order_limit_sell(
            symbol=self.pair,
            quantity=sell_amount,
            price=sell_price,
        )

        return TradeResult(**trade)

    def save_order(
            self,
            order: Order,
            parent_order: bot_models.OrderInfo = None,
    ) -> bot_models.OrderInfo:
        """ Save executed order to database """
        self.logger.debug("Save order #{} to database".format(order.orderId))
        # if we here - order executed and we can save it to the DB
        order_info = bot_models.OrderInfo()
        order_info.pair = order.symbol
        order_info.order_type = order.side
        order_info.amount = order.origQty
        order_info.rate = order.price
        order_info.created = datetime.datetime.now()
        order_info.created_timestamp = datetime.datetime.now()

        if parent_order:
            order_info.parent_order = parent_order

        order_info.save()

        return order_info

    def low_high_daily_prices(self) -> Tuple[Decimal, Decimal]:
        """
        Get low and high daily prices

        :return: tuple low, high
        """
        ticker = Ticker(**self.client.get_ticker(symbol=self.pair))

        return ticker.lowPrice, ticker.highPrice
