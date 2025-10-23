# 자격 검증 로직
# 간단한 예제 작성


def eligibility_check(policy: dict, user: dict) -> str:
    """
    정책의 필수 조건(나이, 지역, 소득 등)을 기반으로 사용자의 자격을 검증
    """
    cond = policy.get("required_conditions", "")
    age = user.get("age", 0)
    region = user.get("region", "")
    income = user.get("income_ratio", 999)

    if "19" in cond and "39" in cond and not (19 <= age <= 39):
        return "연령 미달"
    if "서울" in cond and "서울" not in region:
        return "거주지 불일치"
    if "중위소득" in cond and income > 150:
        return "소득 초과"

    return "지원 가능"
