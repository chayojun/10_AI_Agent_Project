from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from .schema import AnalystResult
from .utils.config import MODEL, TEMPERATURE
from .utils.logger import log


# def llm_reason_with_priority(policy_info: dict, user_info: dict) -> AnalystResult:
#     log("[LLMReasoner] 우대 조건·서류 reasoning 시작")

#     llm = ChatOpenAI(model=MODEL, temperature=TEMPERATURE)
#     parser = PydanticOutputParser(pydantic_object=AnalystResult)

#     prompt = ChatPromptTemplate.from_template(
#         """
#     You are an intelligent policy validation and reasoning agent named "AnalystAgent".

#     Your task is to analyze a government policy description and a user's personal information, then produce a structured JSON response that summarizes:

#     1. Whether the user meets the basic eligibility criteria of the policy.
#     2. Which preferential (priority) conditions, if any, apply to this user.
#     3. Which documents (required and optional) the user must submit.
#     4. A short, human-readable summary that explains the reasoning behind the result.

#     ---

#     ### Instructions
#     - Read the **policy_info** and **user_info** carefully.
#     - Compare all eligibility requirements in the policy (age, region, income ratio, housing status, etc.) with the user’s data.
#     - Identify any **priority_subjects** from the policy that match the user’s situation (e.g., "Seoul resident", "Basic livelihood recipient", etc.).
#     - Based on these matches, determine whether additional documents are required.
#     - Always include both `required_documents` and `optional_documents` lists in your output.
#     - The summary must clearly describe why the user is eligible or not, and mention any applicable priority conditions.

#     ---

#     ### Output Format
#     You must strictly return a valid JSON object that follows this schema:

#     {
#     "eligible": true or false,
#     "matched_priority": [list of applicable priority conditions],
#     "required_documents": [list of required documents],
#     "optional_documents": [list of optional documents],
#     "summary": "A short, clear explanation of the eligibility result and document requirements."
#     }

#     Do not include any text or explanation outside of the JSON object.

#     ---

#     ### Provided Data
#     Policy Information[정책 정보]:
#     {policy_info}

#     User Information[사용자 정보]:
#     {user_info}

#     """
#     )
#     chain = prompt | llm | parser
#     result = chain.invoke(
#         {
#             "policy_info": policy_info,
#             "user_info": user_info,
#             "format_instructions": parser.get_format_instructions(),
#         }
#     )

#     log("[LLMReasoner] reasoning 완료")
#     return result


from .schema import AnalystResult
from .utils.logger import log
from .utils.config import MODEL, TEMPERATURE
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI


def llm_reason_with_priority(
    policy_info: dict, user_info: dict, rule_result: dict
) -> dict:
    """
    LLM 기반 reasoning 단계:
    1. 우대조건 매칭
    2. 제출 서류 확정
    3. 결과 summary 생성
    """

    log("[LLMReasoner] 우대 조건·서류 reasoning 시작")

    # 모델 및 파서 설정
    parser = PydanticOutputParser(pydantic_object=AnalystResult)
    model = ChatOpenAI(model=MODEL, temperature=TEMPERATURE)

    # 프롬프트 템플릿
    prompt = ChatPromptTemplate.from_template(
        """
        You are an intelligent policy validation and reasoning agent named "AnalystAgent".
        Based on the given policy information, user information, and rule-based validation result,
        produce a structured JSON output describing eligibility reasoning.

        ### Instructions
        - If rule_result.eligible is False, keep "eligible": false and explain briefly why.
        - Match any preferential conditions from policy_info["priority_subjects"] that fit the user_info.
        - Always include required_documents and optional_documents lists.
        - Summarize the reasoning in 1–2 concise sentences in Korean.

        ### Output format (strict JSON)
        {{
          "eligible": true or false,
          "matched_priority": [list of applicable priority conditions],
          "required_documents": [list of required documents],
          "optional_documents": [list of optional documents],
          "summary": "Short Korean explanation"
        }}

        ### Inputs
        [Policy Info]
        {policy_info}

        [User Info]
        {user_info}

        [Rule Validation Result]
        {rule_result}

        ### Format instructions
        {format_instructions}
        """
    )

    # 입력 데이터 구성
    input_data = prompt.format_prompt(
        policy_info=policy_info,
        user_info=user_info,
        rule_result=rule_result,
        format_instructions=parser.get_format_instructions(),
    )

    # 모델 호출
    log("[LLMReasoner] Reasoning 요청 중...")
    response = model.invoke(input_data.to_messages())

    # 파싱
    parsed = parser.parse(response.content)
    log("[LLMReasoner] Reasoning 완료 및 결과 파싱 성공")

    return parsed
