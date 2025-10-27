# from .tools_basic import (
#     check_age_tool,
#     check_region_tool,
#     check_income_tool,
#     check_no_house_tool,
# )
# from .utils.logger import log


# def validate_policy(policy_info: dict, user_info: dict) -> dict:
#     """
#     정책 정보(policy_info)와 사용자 정보(user_info)를 비교하여 자격 여부를 판별.
#     """
#     log("[Validator] 기본 정책 검증 시작")

#     results = {
#         "age": check_age_tool.func(user_info.get("age")),
#         "region": check_region_tool.func(user_info.get("region")),
#         "income": check_income_tool.func(user_info.get("income_ratio")),
#         "house": check_no_house_tool.func(user_info.get("house_owned")),
#     }

#     eligible = all(results.values())
#     reasons = [k for k, v in results.items() if not v]

#     log(f"[Validator] 결과: eligible={eligible}, 실패 항목={reasons}")
#     return {"eligible": eligible, "reasons": reasons}


from .tools_basic import (
    check_age_tool,
    check_region_tool,
    check_income_tool,
    check_no_house_tool,
)
from .utils.logger import log
import re


def validate_policy(policy_info: dict, user_info: dict) -> dict:
    """
    정책 정보와 사용자 정보를 비교하여 자격 여부를 판별합니다.
    Args:
        policy_info (dict): SuggestAgent에서 전달받은 정책 JSON
        user_info (dict): 인증서 등에서 얻은 사용자 정보 JSON
    Returns:
        dict: {
            "eligible": bool,
            "reasons": List[str]
        }
    """

    log("[Validator] 기본 정책 검증 시작")

    # -------------------------------------------------
    # 정책 eligibility 문장에서 기준값 파싱
    # 예: "서울시 내 거주 19~39세 이하 청년, 중위소득 150% 이하"
    # -------------------------------------------------
    eligibility_text = policy_info.get("eligibility", "")
    age_min, age_max, income_max = 19, 39, 150  # 기본값

    age_range = re.findall(r"(\d+)\s*~\s*(\d+)", eligibility_text)
    if age_range:
        age_min, age_max = map(int, age_range[0])
    income_match = re.search(r"(\d+)\s*% 이하", eligibility_text)
    if income_match:
        income_max = int(income_match.group(1))

    # -------------------------------------------------
    # 개별 조건 검증 (tool 기반)
    # -------------------------------------------------
    age_ok = check_age_tool.func(user_info["age"], age_min, age_max)
    region_ok = check_region_tool.func(user_info["region"], eligibility_text)
    income_ok = check_income_tool.func(user_info["income_ratio"], income_max)
    house_ok = check_no_house_tool.func(user_info["house_owned"])

    results = {
        "age": age_ok,
        "region": region_ok,
        "income": income_ok,
        "house": house_ok,
    }

    # -------------------------------------------------
    # 종합 판단 및 실패 항목 추출
    # -------------------------------------------------
    eligible = all(results.values())
    reasons = [k for k, v in results.items() if not v]

    # -------------------------------------------------
    # 결과 로그 및 반환
    # -------------------------------------------------
    log(f"[Validator] 결과 → eligible={eligible}, 실패 항목={reasons}")
    return {"eligible": eligible, "reasons": reasons}
