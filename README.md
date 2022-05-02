# Stock Allocation

Calculate quantity of stock to purchase given a custom portfolio allocation and investment value.

```text
Usage: portfolio.py [OPTIONS]

  Stock portfolio allocation calculator.

Options:
  -p, --principal FLOAT  The value of the investment.  [required]
  --help                 Show this message and exit.
```

## Getting Started

To use, create a JSON file named `allocation.json` in the same directory as `portfolio.py`. This document maps each ticker symbol to the proportion (by value) that this stock should represent as part of your portfolio.

Example `allocation.json` file demonstrating a simple 3-fund portfolio.
```json
{
    "VTI": 0.8,
    "VXUS": 0.15,
    "BND": 0.05
}
```

Specify a `principal` value as the amount of money in USD being invested into the portfolio. Example output using the above allocation:
```text
Retrieved prices:
	VTI: 207.36
	VXUS: 55.62
	BND: 75.66
Cost: 3817.97 using transform floor
	VTI: 15
	VXUS: 10
	BND: 2
Cost: 3949.26 using transform around
	VTI: 15
	VXUS: 11
	BND: 3
Cost: 4156.62 using transform ceil
	VTI: 16
	VXUS: 11
	BND: 3
```

## Transformations

To avoid fractional stocks, the script uses 3 float-to-int transformations on the final calculated purchase quantities:
- `floor`: a lower bound on `principal`.
- `around`: will approximate `principal`.
- `ceil`: an upper bound on `principal`.

This yields possible purchase quantities at 3 different price points with `floor <= around <= ceil`.
