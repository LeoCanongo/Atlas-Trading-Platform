def calculate_position_size(account_size, risk_percent, entry_price, stop_loss):
    """
    Calculates the recommended position size based on risk.

    Returns:
        dict
    """

    # Dollar amount willing to risk
    dollar_risk = account_size * (risk_percent / 100)

    # Risk per share
    risk_per_share = abs(entry_price - stop_loss)

    if risk_per_share == 0:
        raise ValueError("Entry price and stop loss cannot be the same.")

    # Number of shares
    shares = int(dollar_risk // risk_per_share)

    # Total position value
    position_value = shares * entry_price

    return {
        "account_size": account_size,
        "risk_percent": risk_percent,
        "dollar_risk": dollar_risk,
        "entry_price": entry_price,
        "stop_loss": stop_loss,
        "risk_per_share": risk_per_share,
        "shares": shares,
        "position_value": position_value,
    }