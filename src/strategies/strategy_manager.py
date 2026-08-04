from src.strategies.trend_strategy import trend_strategy
from src.strategies.breakout_strategy import breakout_strategy
from src.strategies.momentum_strategy import momentum_strategy
from src.strategies.mean_reversion_strategy import mean_reversion_strategy

STRATEGIES = {
    "trend": trend_strategy,
    "breakout": breakout_strategy,
    "momentum": momentum_strategy,
    "mean_reversion": mean_reversion_strategy,
}

ACTIVE_STRATEGY = "trend"


def get_active_strategy():
    return STRATEGIES[ACTIVE_STRATEGY]


def get_active_strategy_name():
    return ACTIVE_STRATEGY


def set_active_strategy(name):
    global ACTIVE_STRATEGY

    if name in STRATEGIES:
        ACTIVE_STRATEGY = name


def get_available_strategies():
    return STRATEGIES