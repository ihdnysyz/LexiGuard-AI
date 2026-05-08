from langchain_core.prompts import ChatPromptTemplate

# 1. 翻译与对齐 Agent (针对跨语种)
translation_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一名精通中英文法律术语的翻译专家。你的任务是将外文合同准确翻译为中文，并标注出两国法律体系中含义不对等的关键词汇。"),
    ("human", "请翻译并分析以下合同条款：\n\n{contract_text}")
])

# 2. 风险识别 Agent
risk_analyst_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一名资深企业法务。请根据合同文本，识别以下风险：1. 责任限制不明确 2. 违约金条款显失公平 3. 司法管辖权争议 4. 知识产权归属模糊。"),
    ("human", "请分析该合同的潜在风险点：\n\n{translated_text}")
])

# 3. 汇总与预警 Agent (CFO/General Counsel 视角)
summarizer_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是首席法务官。请根据翻译内容和风险报告，生成一份面向管理层的 B 端合同摘要，包含：风险等级(高/中/低)、修改建议、以及是否建议签署。"),
    ("human", "翻译内容：{translation}\n风险分析：{risks}")
])
