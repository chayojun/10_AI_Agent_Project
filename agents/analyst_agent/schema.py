from pydantic import BaseModel, Field
from typing import List


class AnalystResult(BaseModel):
    """AnalystAgent 최종 JSON 출력 구조"""

    eligible: bool = Field(..., description="정책 자격 충족 여부")
    matched_priority: List[str] = Field(
        default_factory=list, description="우대 조건 일치 목록"
    )
    required_documents: List[str] = Field(
        default_factory=list, description="필수 서류 목록"
    )
    optional_documents: List[str] = Field(
        default_factory=list, description="선택 서류 목록"
    )
    summary: str = Field(..., description="최종 요약 설명 (자연어)")
