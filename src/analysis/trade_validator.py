class TradeValidator:

    MIN_RISK_REWARD = 2.0
    MIN_TARGET_DISTANCE = 2.0      # %
    MAX_STOP_DISTANCE = 5.0        # %

    @staticmethod
    def validate(entry, stop, target):

        errors = []

        if stop >= entry:
            errors.append(
                "Stop loss must be below entry price."
            )

        if target <= entry:
            errors.append(
                "Target must be above entry price."
            )

        if len(errors) > 0:
            return {
                "valid": False,
                "errors": errors,
            }

        risk = entry - stop
        reward = target - entry

        rr = reward / risk

        if rr < TradeValidator.MIN_RISK_REWARD:

            errors.append(
                f"Risk/Reward ({rr:.2f}) is below "
                f"{TradeValidator.MIN_RISK_REWARD:.1f}:1"
            )

        target_distance = (
            reward / entry
        ) * 100

        if target_distance < TradeValidator.MIN_TARGET_DISTANCE:

            errors.append(
                "Profit target is too close."
            )

        stop_distance = (
            risk / entry
        ) * 100

        if stop_distance > TradeValidator.MAX_STOP_DISTANCE:

            errors.append(
                "Stop loss is too far away."
            )

        return {
            "valid": len(errors) == 0,
            "risk": round(risk, 2),
            "reward": round(reward, 2),
            "risk_reward": round(rr, 2),
            "target_distance": round(target_distance, 2),
            "stop_distance": round(stop_distance, 2),
            "errors": errors,
        }