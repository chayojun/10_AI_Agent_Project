# 우대조건 탐색


def priority_match(policy: dict, user: dict) -> str:
    """
    정책의 우대 조건(예: 1인 가구, 저소득층 등)에 따라 유형 결정
    """

    optional = policy.get("optional_conditions", [])
    if "1인 가구" in optional and user.get("household_type") == "1인 가구":
        return "1인 가구 우대형"
    if "저소득" in optional and user.get("income_ratio", 999) <= 100:
        return "저소득 우대형"
    return "일반형"
