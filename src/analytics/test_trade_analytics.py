from src.analytics.trade_analytics import get_trade_statistics

stats = get_trade_statistics()

print("=" * 40)
print("ATLAS TRADE ANALYTICS")
print("=" * 40)

for key, value in stats.items():

    if isinstance(value, float):
        print(f"{key}: {value:.2f}")

    else:
        print(f"{key}: {value}")