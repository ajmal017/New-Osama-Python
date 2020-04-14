from zipline.api import order, symbol
from zipline.finance import commission, slippage

stocks = ['AAPL', 'MSFT']


def initialize(context):
    context.has_ordered = False
    context.stocks = stocks

    # Explicitly set the commission/slippage to the "old" value until we can
    # rebuild example data.
    # github.com/quantopian/zipline/blob/master/tests/resources/
    # rebuild_example_data#L105
    context.set_commission(commission.PerShare(cost=.0075, min_trade_cost=1.0))
    context.set_slippage(slippage.VolumeShareSlippage())


def handle_data(context, data):
    if not context.has_ordered:
        for stock in context.stocks:
            order(symbol(stock), 100)
        context.has_ordered = True


def _test_args():
    """Extra arguments to use when zipline's automated tests run this example.
    """
    import pandas as pd

    return {
        'start': pd.Timestamp('2008', tz='utc'),
        'end': pd.Timestamp('2013', tz='utc'),
    }