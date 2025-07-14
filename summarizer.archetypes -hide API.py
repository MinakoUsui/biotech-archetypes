import pandas as pd
import openai
import os

# 🔐 Insert your OpenAI API key
openai.api_key = "sk----"  # Replace with your actual key

# 📁 Load CSV file
file_name = "biotech_mna_deals.csv"
if not os.path.exists(file_name):
    print(f"❌ File not found: {file_name}")
    exit()

# 📄 Read first 20 rows
df = pd.read_csv(file_name).head(20)
summaries = []

# 🔁 Process each deal
for index, row in df.iterrows():
    # Clean inputs
    deal_value_str = str(row['Total consideration']).replace("$", "").replace(",", "")
    premium_str = str(row['Premium']).replace("%", "").replace("N/A", "").strip()

    try:
        deal_value = float(deal_value_str)
    except ValueError:
        deal_value = 0

    try:
        premium = float(premium_str)
    except ValueError:
        premium = 0

    # 📌 Strategic tags
    tags = []
    if deal_value >= 1000:
        tags.append("🟢 High-value deal ($1B+)")
    if premium >= 100:
        tags.append("🔥 Premium >100%")
    if premium >= 150 or "unicorn" in str(row['Company acquired']).lower():
        tags.append("🦄 Potential unicorn")
    tag_text = " | ".join(tags) if tags else "Standard deal"

    # ✍️ Investor memo
    summary_prompt = f"""
    Summarize this biotech M&A deal in no more than 5 sentences. Be concise and strategic.
    Acquirer: {row['Acquirer']}
    Target: {row['Company acquired']}
    Date: {row['Date of deal']}
    Deal Value: {row['Total consideration']}
    Price Per Share: {row['Price per share']}
    Premium: {row['Premium']}
    """
    summary_response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": summary_prompt}],
        temperature=0.5
    )
    summary = summary_response.choices[0].message.content

    # 🧬 Startup archetype
    archetype_prompt = f"""
    Give a 1–2 sentence startup archetype for {row['Company acquired']}. Include platform traits and strategic positioning.
    """
    archetype_response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": archetype_prompt}],
        temperature=0.5
    )
    archetype = archetype_response.choices[0].message.content

    # 👤 Founder persona
    founder_prompt = f"""
    Describe the founder of {row['Company acquired']} in 3 sentences: background, motivation, and leadership style. Keep it focused and relevant to the acquisition by {row['Acquirer']}.
    """
    founder_response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": founder_prompt}],
        temperature=0.6
    )
    founder_persona = founder_response.choices[0].message.content

    # 🎨 Style scoring
    style_prompt = f"""
    Based on the founder persona below, list up to 3 style traits using bullets. Choose from: Mission-Driven, Platform-Technical, Narrative-Aware, Challenger Energy, Founder Discipline. Justify each in one sentence.

    Founder Persona:
    {founder_persona}
    """
    style_response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": style_prompt}],
        temperature=0.5
    )
    style_scores = style_response.choices[0].message.content

    # 📝 Assemble memo block
    memo = f"""### Deal {index+1}: {row['Acquirer']} → {row['Company acquired']}
**Tags**: {tag_text}

## Investor Memo
{summary}

## Startup Archetype
{archetype}

## Founder Persona
{founder_persona}

## Style Scoring
{style_scores}

---
"""
    summaries.append(memo)
    print(f"✅ Deal {index+1} processed.")

# 💾 Save markdown file
output_file = "biotech_archetypes_20.md"
with open(output_file, "w", encoding="utf-8") as file:
    file.write("\n".join(summaries))

print(f"\n📎 Results saved to `{output_file}`")