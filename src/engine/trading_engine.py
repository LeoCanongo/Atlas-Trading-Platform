import time


def run_engine(interval=30):

    from src.engine.bot_controller import bot_running
    from src.paper_trading.auto_trader import main

    print("=" * 50)
    print("ATLAS TRADING ENGINE")
    print("=" * 50)

    while bot_running():

        print("\nStarting Trading Cycle...\n")

        try:
            main()

        except Exception as e:
            print(f"ERROR: {e}")

        if not bot_running():
            break

        print(f"\nSleeping {interval} seconds...\n")

        for _ in range(interval):

            if not bot_running():
                break

            time.sleep(1)

    print("\nTrading engine stopped.")