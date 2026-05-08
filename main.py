import operator
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, END
from agents import translation_prompt, risk_analyst_prompt, summarizer_prompt
from langchain_openai import ChatOpenAI

# 定义状态流转的数据结构
class AgentState(TypedDict):
    raw_text: str
    translation: str
    risks: str
    final_report: str

llm = ChatOpenAI(model="deepseek-chat", temperature=0)

# 节点逻辑
def translation_node(state: AgentState):
    response = llm.invoke(translation_prompt.format(contract_text=state["raw_text"]))
    return {"translation": response.content}

def risk_analysis_node(state: AgentState):
    response = llm.invoke(risk_analyst_prompt.format(translated_text=state["translation"]))
    return {"risks": response.content}

def summary_node(state: AgentState):
    response = llm.invoke(summarizer_prompt.format(
        translation=state["translation"], 
        risks=state["risks"]
    ))
    return {"final_report": response.content}

# 构建图
workflow = StateGraph(AgentState)

workflow.add_node("translator", translation_node)
workflow.add_node("analyst", risk_analysis_node)
workflow.add_node("summarizer", summary_node)

workflow.set_entry_point("translator")
workflow.add_edge("translator", "analyst")
workflow.add_edge("analyst", "summarizer")
workflow.add_edge("summarizer", END)

app_graph = workflow.compile()
