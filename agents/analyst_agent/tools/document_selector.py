# 서류 리스트 생성


def document_selector(policy: dict, priority_type: str) -> list:
    """
    필수 서류 + 우대형 서류 조합 결정
    """
    base_docs = policy.get("required_documents", [])
    result = base_docs.copy()

    if "우대" in priority_type:
        result.append("우대 증빙서류")

    return result
