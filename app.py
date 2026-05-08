import streamlit as st
from main import app_graph

st.set_page_config(page_title="AI 跨语种法律合同审查", layout="wide")

st.title("⚖️ 多 Agent 跨语种法律合同智能审查系统")
st.info("适合 B 端企业服务：支持中英双语，涵盖翻译、合规性检查与风险分级。")

col1, col2 = st.columns(2)

with col1:
    contract_input = st.text_area("粘贴合同原文 (Chinese/English):", height=400)
    if st.button("开始智能审查"):
        if contract_input:
            with st.spinner("多 Agent 协作中..."):
                initial_state = {"raw_text": contract_input}
                result = app_graph.invoke(initial_state)
                st.session_state['result'] = result
        else:
            st.warning("请输入合同内容")

if 'result' in st.session_state:
    res = st.session_state['result']
    with col2:
        st.subheader("📋 最终审查报告")
        st.markdown(res['final_report'])
        
        with st.expander("查看翻译对齐"):
            st.write(res['translation'])
        with st.expander("查看详细风险点"):
            st.write(res['risks'])
