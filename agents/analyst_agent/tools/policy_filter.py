# 정책 청년 여부 필터링


# 일단 청년인지 아닌지만 확인
def policy_filter(policy: dict) -> bool:
    """정책명이 '청년' 관련 정책인지 확인"""
    name = policy.get("policy_name", "")
    return "청년" in name or "Youth" in name
