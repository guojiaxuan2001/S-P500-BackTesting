# S&P 500 Mean Reversion Trading Strategy Backtesting System

A Python-based quantitative trading strategy backtesting system that implements a mean reversion trading strategy for S&P 500 constituents.

## Strategy Overview

The strategy is based on mean reversion theory with the following core logic:
1. Select the 10 stocks with the largest daily price drops from S&P 500 constituents
2. Invest equally in these 10 stocks
3. Close positions after one day and repeat the process

## Project Structure

```
├── mean_reversion_strategy.py  # Main strategy implementation
├── strategy_comparison.py      # Strategy vs market comparison
├── spx-companies.csv          # S&P 500 constituents data
├── portfolio_values.csv       # Strategy performance data
├── trading_records.csv        # Trading records
└── strategy_comparison.png    # Strategy comparison visualization
```

## Requirements

- Python 3.12+
- pandas
- numpy
- yfinance
- matplotlib

## Performance

Strategy performance over the past two years:

- Total Return: 140.94%
- Annual Volatility: 26.13%
- Sharpe Ratio: 1.77

S&P 500 performance over the same period:
- Total Return: 43.38%
- Annual Volatility: 16.13%
- Sharpe Ratio: 1.08

## Risk Disclaimer

- Past performance does not guarantee future returns
- Backtesting results do not include transaction costs and slippage
- Live trading may face liquidity risks
- Strategy performance may vary in different market conditions

## Future Improvements
Future extensions will involve leveraging LLMs for automated financial report extraction and interpretation, aiming to refine and augment the trading decision-making process.


## Contributing

Issues and Pull Requests are welcome to help improve this project.

## License

MIT License
