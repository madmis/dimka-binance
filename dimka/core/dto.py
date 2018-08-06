from decimal import Decimal


class BaseSymbolDTO(object):
    def __init__(self, symbol: str):
        self.symbol = symbol

    @property
    def symbol(self) -> str:
        return self._symbol

    @symbol.setter
    def symbol(self, value: str):
        self._symbol = value


class BaseOrder(BaseSymbolDTO):
    def __init__(
            self,
            symbol: str,
            orderId: int,
            clientOrderId: str,
            price: float,
            origQty: float,
            executedQty: float,
            cummulativeQuoteQty: float,
            status: str,
            timeInForce: str,
            type: str,
            side: str,
    ):
        super().__init__(symbol)
        self.orderId = orderId
        self.clientOrderId = clientOrderId
        self.price = price
        self.origQty = origQty
        self.executedQty = executedQty
        self.cummulativeQuoteQty = cummulativeQuoteQty
        self.status = status
        self.timeInForce = timeInForce
        self.type = type
        self.side = side

    @property
    def orderId(self) -> int:
        return self._orderId

    @orderId.setter
    def orderId(self, value: int):
        self._orderId = int(value)

    @property
    def clientOrderId(self) -> str:
        return self._clientOrderId

    @clientOrderId.setter
    def clientOrderId(self, value: str):
        self._clientOrderId = value

    @property
    def price(self) -> Decimal:
        return self._price

    @price.setter
    def price(self, value: float):
        self._price = Decimal(value)

    @property
    def origQty(self) -> Decimal:
        return self._origQty

    @origQty.setter
    def origQty(self, value: float):
        self._origQty = Decimal(value)

    @property
    def executedQty(self) -> Decimal:
        return self._executedQty

    @executedQty.setter
    def executedQty(self, value: float):
        self._executedQty = Decimal(value)

    @property
    def cummulativeQuoteQty(self) -> Decimal:
        return self._cummulativeQuoteQty

    @cummulativeQuoteQty.setter
    def cummulativeQuoteQty(self, value: float):
        self._cummulativeQuoteQty = Decimal(value)

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str):
        self._status = value

    @property
    def timeInForce(self) -> str:
        return self._timeInForce

    @timeInForce.setter
    def timeInForce(self, value: str):
        self._timeInForce = value

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, value: str):
        self._type = value

    @property
    def side(self) -> str:
        return self._side

    @side.setter
    def side(self, value: str):
        self._side = value


class PairInfo(BaseSymbolDTO):
    def __init__(
            self,
            symbol: str,
            status: str,
            baseAsset: str,
            baseAssetPrecision: int,
            quoteAsset: int,
            quotePrecision: int,
            orderTypes: list,
            icebergAllowed: bool,
            filters: list,
    ):
        super().__init__(symbol)
        self.status = status
        self.baseAsset = baseAsset
        self.baseAssetPrecision = baseAssetPrecision
        self.quoteAsset = quoteAsset
        self.quotePrecision = quotePrecision
        self.orderTypes = orderTypes
        self.icebergAllowed = icebergAllowed
        self.filters = filters

        self._extractFilters()

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str):
        self._status = value

    @property
    def baseAsset(self) -> str:
        return self._baseAsset

    @baseAsset.setter
    def baseAsset(self, value: str):
        self._baseAsset = value

    @property
    def baseAssetPrecision(self) -> int:
        return self._baseAssetPrecision

    @baseAssetPrecision.setter
    def baseAssetPrecision(self, value: int):
        self._baseAssetPrecision = int(value)

    @property
    def quoteAsset(self) -> str:
        return self._quoteAsset

    @quoteAsset.setter
    def quoteAsset(self, value: str):
        self._quoteAsset = value

    @property
    def quotePrecision(self) -> int:
        return self._quotePrecision

    @quotePrecision.setter
    def quotePrecision(self, value: int):
        self._quotePrecision = int(value)

    @property
    def orderTypes(self) -> list:
        return self._orderTypes

    @orderTypes.setter
    def orderTypes(self, value: list):
        self._orderTypes = value

    @property
    def icebergAllowed(self) -> bool:
        return self._icebergAllowed

    @icebergAllowed.setter
    def icebergAllowed(self, value: bool):
        self._icebergAllowed = bool(value)

    @property
    def filters(self) -> list:
        return self._filters

    @filters.setter
    def filters(self, value: list):
        self._filters = value

    @property
    def minPrice(self) -> Decimal:
        return self._minPrice

    @minPrice.setter
    def minPrice(self, value: float):
        self._minPrice = Decimal(value)

    @property
    def maxPrice(self) -> Decimal:
        return self._maxPrice

    @maxPrice.setter
    def maxPrice(self, value: float):
        self._maxPrice = Decimal(value)

    @property
    def tickSize(self) -> Decimal:
        return self._tickSize

    @tickSize.setter
    def tickSize(self, value: float):
        self._tickSize = Decimal(value)

    @property
    def minAmount(self) -> Decimal:
        return self._minAmount

    @minAmount.setter
    def minAmount(self, value: float):
        self._minAmount = Decimal(value)

    def _extractFilters(self):
        price = None
        notional = None

        for item in self.filters:
            if item["filterType"] == "PRICE_FILTER":
                price = item
                continue
            if item["filterType"] == "MIN_NOTIONAL":
                notional = item
                continue

        if not price:
            InsufficientDataException(
                'Unable find filter "PRICE_FILTER" for pair: {}'.format(self.symbol)
            )

        if not notional:
            InsufficientDataException(
                'Unable find filter "MIN_NOTIONAL" for pair: {}'.format(self.symbol)
            )

        self.minPrice = Decimal(price["minPrice"])
        self.maxPrice = Decimal(price["maxPrice"])
        self.tickSize = Decimal(price["tickSize"])
        self.minAmount = Decimal(notional["minNotional"])


class Order(BaseOrder):
    def __init__(
            self,
            symbol: str,
            orderId: int,
            clientOrderId: str,
            price: float,
            origQty: float,
            executedQty: float,
            cummulativeQuoteQty: float,
            status: str,
            timeInForce: str,
            type: str,
            side: str,
            stopPrice: float,
            icebergQty: float,
            time: int,
            updateTime: int,
            isWorking: bool,
    ):
        super().__init__(
            symbol,
            orderId,
            clientOrderId,
            price,
            origQty,
            executedQty,
            cummulativeQuoteQty,
            status,
            timeInForce,
            type,
            side,
        )
        self.stopPrice = stopPrice
        self.icebergQty = icebergQty
        self.time = time
        self.updateTime = updateTime
        self.isWorking = isWorking

    @property
    def stopPrice(self) -> Decimal:
        return self._stopPrice

    @stopPrice.setter
    def stopPrice(self, value: float):
        self._stopPrice = Decimal(value)

    @property
    def icebergQty(self) -> Decimal:
        return self._icebergQty

    @icebergQty.setter
    def icebergQty(self, value: float):
        self._icebergQty = Decimal(value)

    @property
    def time(self) -> int:
        return self._time

    @time.setter
    def time(self, value: int):
        self._time = int(value)

    @property
    def updateTime(self) -> int:
        return self._updateTime

    @updateTime.setter
    def updateTime(self, value: int):
        self._updateTime = int(value)

    @property
    def isWorking(self) -> bool:
        return self._isWorking

    @isWorking.setter
    def isWorking(self, value: bool):
        self._isWorking = bool(value)


class BookTicker(BaseSymbolDTO):
    def __init__(
            self,
            symbol: str,
            bidPrice: float,
            bidQty: float,
            askPrice: float,
            askQty: float,
    ):
        super().__init__(symbol=symbol)
        self.bidPrice = bidPrice
        self.bidQty = bidQty
        self.askPrice = askPrice
        self.askQty = askQty

    @property
    def bidPrice(self) -> Decimal:
        return self._bidPrice

    @bidPrice.setter
    def bidPrice(self, value: float):
        self._bidPrice = Decimal(value)

    @property
    def bidQty(self) -> Decimal:
        return self._bidQty

    @bidQty.setter
    def bidQty(self, value: float):
        self._bidQty = Decimal(value)

    @property
    def askPrice(self) -> Decimal:
        return self._askPrice

    @askPrice.setter
    def askPrice(self, value: float):
        self._askPrice = Decimal(value)

    @property
    def askQty(self) -> Decimal:
        return self._askQty

    @askQty.setter
    def askQty(self, value: float):
        self._askQty = Decimal(value)


class TradeResult(BaseOrder):
    def __init__(
            self,
            symbol: str,
            orderId: int,
            clientOrderId: str,
            transactTime: int,
            price: float,
            origQty: float,
            executedQty: float,
            cummulativeQuoteQty: float,
            status: str,
            timeInForce: str,
            type: str,
            side: str,
            fills: list,
    ):
        super().__init__(
            symbol,
            orderId,
            clientOrderId,
            price,
            origQty,
            executedQty,
            cummulativeQuoteQty,
            status,
            timeInForce,
            type,
            side,
        )
        self.transactTime = transactTime
        self.fills = fills

    @property
    def transactTime(self) -> int:
        return self._transactTime

    @transactTime.setter
    def transactTime(self, value: int):
        self._transactTime = int(value)

    @property
    def fills(self) -> list:
        return self._fills

    @fills.setter
    def fills(self, value: list):
        self._fills = value


class Ticker(BaseSymbolDTO):
    def __init__(
            self,
            symbol: str,
            priceChange: float,
            priceChangePercent: float,
            weightedAvgPrice: float,
            prevClosePrice: float,
            lastPrice: float,
            lastQty: float,
            bidPrice: float,
            askPrice: float,
            openPrice: float,
            highPrice: float,
            lowPrice: float,
            volume: float,
            quoteVolume: float,
            openTime: int,
            closeTime: int,
            firstId: int,
            lastId: int,
            count: int,
    ):
        super().__init__(symbol)
        self.priceChange = priceChange

        self.priceChangePercent = priceChangePercent
        self.weightedAvgPrice = weightedAvgPrice
        self.prevClosePrice = prevClosePrice
        self.lastPrice = lastPrice
        self.lastQty = lastQty
        self.bidPrice = bidPrice
        self.askPrice = askPrice
        self.openPrice = openPrice
        self.highPrice = highPrice
        self.lowPrice = lowPrice
        self.volume = volume
        self.quoteVolume = quoteVolume
        self.openTime = openTime
        self.closeTime = closeTime
        self.firstId = firstId
        self.lastId = lastId
        self.count = count

    @property
    def priceChange(self) -> Decimal:
        return self._priceChange

    @priceChange.setter
    def priceChange(self, value: float):
        self._priceChange = Decimal(value)

    @property
    def priceChangePercent(self) -> Decimal:
        return self._priceChangePercent

    @priceChangePercent.setter
    def priceChangePercent(self, value: float):
        self._priceChangePercent = Decimal(value)

    @property
    def weightedAvgPrice(self) -> Decimal:
        return self._weightedAvgPrice

    @weightedAvgPrice.setter
    def weightedAvgPrice(self, value: float):
        self._weightedAvgPrice = Decimal(value)

    @property
    def prevClosePrice(self) -> Decimal:
        return self._prevClosePrice

    @prevClosePrice.setter
    def prevClosePrice(self, value: float):
        self._prevClosePrice = Decimal(value)

    @property
    def lastPrice(self) -> Decimal:
        return self._lastPrice

    @lastPrice.setter
    def lastPrice(self, value: float):
        self._lastPrice = Decimal(value)

    @property
    def lastQty(self) -> Decimal:
        return self._lastQty

    @lastQty.setter
    def lastQty(self, value: float):
        self._lastQty = Decimal(value)

    @property
    def bidPrice(self) -> Decimal:
        return self._bidPrice

    @bidPrice.setter
    def bidPrice(self, value: float):
        self._bidPrice = Decimal(value)

    @property
    def askPrice(self) -> Decimal:
        return self._askPrice

    @askPrice.setter
    def askPrice(self, value: float):
        self._askPrice = Decimal(value)

    @property
    def openPrice(self) -> Decimal:
        return self._openPrice

    @openPrice.setter
    def openPrice(self, value: float):
        self._openPrice = Decimal(value)

    @property
    def highPrice(self) -> Decimal:
        return self._highPrice

    @highPrice.setter
    def highPrice(self, value: float):
        self._highPrice = Decimal(value)

    @property
    def lowPrice(self) -> Decimal:
        return self._lowPrice

    @lowPrice.setter
    def lowPrice(self, value: float):
        self._lowPrice = Decimal(value)

    @property
    def volume(self) -> Decimal:
        return self._volume

    @volume.setter
    def volume(self, value: float):
        self._volume = Decimal(value)

    @property
    def quoteVolume(self) -> Decimal:
        return self._quoteVolume

    @quoteVolume.setter
    def quoteVolume(self, value: float):
        self._quoteVolume = Decimal(value)

    @property
    def openTime(self) -> int:
        return self._openTime

    @openTime.setter
    def openTime(self, value: int):
        self._openTime = int(value)

    @property
    def closeTime(self) -> int:
        return self._closeTime

    @closeTime.setter
    def closeTime(self, value: int):
        self._closeTime = int(value)

    @property
    def firstId(self) -> int:
        return self._firstId

    @firstId.setter
    def firstId(self, value: int):
        self._firstId = int(value)

    @property
    def lastId(self) -> int:
        return self._lastId

    @lastId.setter
    def lastId(self, value: int):
        self._lastId = int(value)

    @property
    def count(self) -> int:
        return self._count

    @count.setter
    def count(self, value: int):
        self._count = int(value)


class InsufficientDataException(RuntimeError):
    """
    Exception when data from response is not enough to init DTO object
     """
    pass
