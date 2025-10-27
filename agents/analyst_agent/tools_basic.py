# # 단일 검증 함수 (@tool 기반)

# from langchain.tools import tool
# from utils.logger import log


# @tool("check_age")
# def check_age_tool(age: int, min_age: int, max_age: int) -> bool:
#     """나이 요건 검증"""
#     log(f"check_age 실행: {age}세 (기준 {min_age}~{max_age})")
#     return min_age <= age <= max_age


# @tool("check_income")
# def check_income_tool(income: int, limit_ratio: int) -> bool:
#     """소득 기준 검증"""
#     log(f"check_income 실행: {income}% / 기준 {limit_ratio}%")
#     return income <= limit_ratio


# @tool("check_region")
# def check_region_tool(region: str, required_region: str) -> bool:
#     """거주지 검증"""
#     log(f"check_region 실행: {region} / 기준 {required_region}")
#     return required_region in region


# @tool("check_no_house")
# def check_no_house_tool(has_house: bool) -> bool:
#     """무주택자 여부 검증"""
#     log(f"check_no_house 실행: {has_house}")
#     return not has_house


from langchain.tools import tool
from .utils.logger import log


# 나이 검증
@tool("check_age")
def check_age_tool(user_age: int, min_age: int = 19, max_age: int = 39) -> bool:
    """사용자가 정책 기준 나이 범위 내에 있는지 검증"""
    result = min_age <= user_age <= max_age
    log(f"[Tool] 나이 검증 실행: {user_age}세 → 기준 {min_age}~{max_age} → {result}")
    return result


# 거주지 검증
@tool("check_region")
def check_region_tool(user_region: str, eligibility_text: str = "서울") -> bool:
    """정책의 거주지 요건(예: '서울시 거주')을 만족하는지 검증"""
    result = any(
        keyword in user_region for keyword in ["서울", "Seoul", "관악", "Gwanak"]
    )
    log(f"[Tool] 지역 검증 실행: {user_region} → {result}")
    return result


# 중위소득 비율 검증
@tool("check_income")
def check_income_tool(user_income_ratio: int, max_income_ratio: int = 150) -> bool:
    """사용자의 중위소득 비율이 정책 기준 이하인지 검증"""
    result = user_income_ratio <= max_income_ratio
    log(
        f"[Tool] 소득 검증 실행: {user_income_ratio}% / 기준 {max_income_ratio}% → {result}"
    )
    return result


# 무주택자인지에 대한 검증
@tool("check_no_house")
def check_no_house_tool(has_house: bool) -> bool:
    """사용자가 무주택자인지 검증"""
    result = not has_house
    log(f"[Tool] 무주택 검증 실행: {has_house} → {result}")
    return result
