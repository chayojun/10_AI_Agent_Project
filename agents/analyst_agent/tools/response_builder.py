# 최종 결과 조립


def build_response(policy, eligibility, priority, documents):
    """최종 JSON 출력"""
    return {
        "policy_name": policy.get("policy_name"),
        "eligibility_result": eligibility,
        "priority_type": priority,
        "required_documents": documents,
        "message": f"{policy.get('policy_name')} 정책에 {eligibility}합니다. ({priority})",
    }
