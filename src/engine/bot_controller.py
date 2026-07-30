import threading

from src.engine.trading_engine import run_engine
from src.paper_trading.auto_trader import main

_engine_thread = None
_running = False


def start_bot():

    global _engine_thread
    global _running

    if _running:
        return False

    _running = True

    def worker():
        global _running

        try:
            run_engine()

        finally:
            _running = False

    _engine_thread = threading.Thread(
        target=worker,
        daemon=True,
    )

    _engine_thread.start()

    return True


def stop_bot():

    global _running

    _running = False

    return True


def run_once():

    main()


def bot_running():

    return _running