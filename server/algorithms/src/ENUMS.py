from enum import Enum

class Strategies(Enum):
    SHORT = 1
    MEDIUM = 2
    LONG = 3
    
    SHORT_LOW_RISK = 1
    MEDIUM_LOW_RISK = 2
    LONG_LOW_RISK = 3

    SHORT_MEDIUM_RISK = 4
    MEDIUM_MEDIUM_RISK = 5
    LONG_MEDIUM_RISK = 6

    SHORT_HIGH_RISK = 7
    MEDIUM_HIGH_RISK = 8
    LONG_HIGH_RISK = 9

class Risk(Enum):
    SHORT_LOW_RISK = 1
    MEDIUM_LOW_RISK = 2
    LONG_LOW_RISK = 3

    SHORT_MEDIUM_RISK = 4
    MEDIUM_MEDIUM_RISK = 5
    LONG_MEDIUM_RISK = 6

    SHORT_HIGH_RISK = 7
    MEDIUM_HIGH_RISK = 8
    LONG_HIGH_RISK = 9


class DH_API(Enum):
    ALPACA = 1

    BINANCE = 2
    POLYGON = 3
    IBKR = 4
    ALPHA = 5


class EH_API(Enum):
    ALPACA = 1

    BINANCE = 2
    IBKR = 3
    ALPHA = 4

class Stop_loss(Enum):
    RSI = 1
    STATIC = 2
