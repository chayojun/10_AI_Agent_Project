# AnalystAgentTool (Supervisor가 호출)
from typing import Type
from langchain_core.tools import BaseTool
from pydantic import BaseModel
from .utils.logger import log
from .validator import validate_policy
from .llm_reasoner import llm_reason_with_priority


class AnalystInput(BaseModel):
    policy_info: dict
    user_info: dict


class AnalystAgentTool(BaseTool):
    name: str = "analyst_agent"
    description: str = (
        "정책 자격 검증 및 우대조건·서류 리스트 판단을 수행하는 Analyst Agent"
    )
    args_schema: Type[BaseModel] = AnalystInput

    def _run(self, policy_info: dict, user_info: dict) -> dict:
        """
        1. Rule-based 검증
        2. LLM reasoning( 우대조건 , 서류, 요약)
        """
        log("[AnalystAgent] 실행 시작")

        # 1단계. Rule 검증
        rule_result = validate_policy(policy_info, user_info)

        if not rule_result["eligible"]:
            log("[AnalystAgent] 자격 미충족 - LLM 단계 건너뜀")
            return {
                "eligible": False,
                "matched_priority": [],
                "required_documents": [],
                "optional_documents": [],
                "summary": "지원 불가: " + ", ".join(rule_result["reasons"]),
            }

        # Step 2. LLM 기반 reasoning 수행

        llm_result = llm_reason_with_priority(policy_info, user_info, rule_result)

        log("[AnalystAgent] 검증 완료 - JSON 결과 반환")
        return llm_result
