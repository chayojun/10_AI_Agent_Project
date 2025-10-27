# 여러 @tool 묶어서 Toolkit 구성

from langchain.agents.agent_toolkits.base import BaseToolkit
from .tools_basic import (
    check_age_tool,
    check_income_tool,
    check_region_tool,
    check_no_house_tool,
)
from .utils.logger import log


class AnalystToolkit(BaseToolkit):
    """AnalystAgent 내부 검증용 Tool 세트"""

    def get_tools(self):
        log("AnalystToolkit 로드 됨")
        return [
            check_age_tool,
            check_income_tool,
            check_region_tool,
            check_no_house_tool,
        ]
