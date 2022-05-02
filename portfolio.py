"""Stock portfolio allocation calculator."""
from typing import Any, Callable, Dict, Iterable, Tuple
from math import isclose
from json import load
from concurrent.futures import ThreadPoolExecutor
from yfinance import Ticker  # type: ignore
import numpy as np  # type: ignore
from click import command, option
# pylint: disable=no-value-for-parameter

ArrayFunc = Callable[[np.ndarray], np.ndarray]


def parse_input(portfolio: dict) -> Tuple[np.ndarray, np.ndarray]:
    """Check input and parse into numpy arrays."""
    for key, value in portfolio.items():
        assert isinstance(key, str), f'Key {key} must be a string.'
        assert isinstance(value, float), f'Value {value} must be a float.'
    symbol = np.array(list(portfolio))
    allocation = np.fromiter(portfolio.values(), dtype=float)
    assert isclose(np.sum(allocation), 1.0), 'Sum of values must be 1.'
    return symbol, allocation


def curr_price(sym: str) -> float:
    """Retrieve current stock price given the symbol."""
    tick = Ticker(sym)
    today = tick.history(period='1d')
    return today['Close'][0]


def indented_enumerate(left: Iterable[Any], right: Iterable[Any]):
    """Print two collections with indentation."""
    for key, value in zip(left, right):
        print(f'\t{key}: {value}')


@command()
@option('--principal', '-p', type=float, required=True,
        help='The value of the investment.')
def main(principal: float):
    """Stock portfolio allocation calculator."""
    with open('allocation.json', encoding='utf-8') as fin:
        portfolio: Dict[str, float] = load(fin)
    symbol, allocation = parse_input(portfolio)
    with ThreadPoolExecutor(min(8, len(symbol))) as pool:
        fut = pool.map(curr_price, symbol)
    price = np.fromiter(fut, dtype=float)
    print('Retrieved prices:')
    indented_enumerate(symbol, np.around(price, 2))
    quantity = principal * allocation / price
    transform: Tuple[ArrayFunc, ...] = (np.floor, np.around, np.ceil)
    for mapping in transform:
        buy = mapping(quantity).astype(int)
        total = round(price @ buy, 2)
        print('Cost:', total, 'using transform', mapping.__name__)
        indented_enumerate(symbol, buy)


if __name__ == '__main__':
    main()
