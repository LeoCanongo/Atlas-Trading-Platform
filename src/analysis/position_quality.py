class PositionQuality:

    @staticmethod
    def evaluate(entry, stop, target):

        risk = entry - stop
        reward = target - entry

        if risk <= 0:
            return {
                "risk": 0,
                "reward": 0,
                "rr": 0,
                "grade": "INVALID",
            }

        rr = reward / risk

        if rr >= 4:
            grade = "A+"
        elif rr >= 3:
            grade = "A"
        elif rr >= 2:
            grade = "B"
        elif rr >= 1.5:
            grade = "C"
        else:
            grade = "D"

        return {
            "risk": round(risk, 2),
            "reward": round(reward, 2),
            "rr": round(rr, 2),
            "grade": grade,
        }