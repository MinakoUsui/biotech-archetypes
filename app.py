import streamlit as st
import re

# 📁 Load your Markdown file
with open("biotech_archetypes_20.md", "r", encoding="utf-8") as f:
    content = f.read()

st.set_page_config(page_title="Biotech Archetype Explorer", layout="wide")
st.title("🧬 Biotech Archetype Explorer")
st.write("Browse 20 founder narratives, investor memos, and startup profiles.")

# 🔍 Extract individual deal blocks
deal_blocks = re.split(r'\n---\n', content)

# 🧠 Parse acquirer names for filtering
acquirers = []
for block in deal_blocks:
    match = re.search(r'Deal \d+: (\w.+?) →', block)
    if match:
        acquirers.append(match.group(1))

unique_acquirers = sorted(list(set(acquirers)))
selected_acquirer = st.sidebar.selectbox("🔍 Filter by Acquirer", ["All"] + unique_acquirers)

# 📄 Display filtered deals
for block in deal_blocks:
    match = re.search(r'Deal \d+: (\w.+?) →', block)
    if match:
        acquirer = match.group(1)
        if selected_acquirer != "All" and acquirer != selected_acquirer:
            continue

    with st.expander(match.group(0)):
        st.markdown(block)