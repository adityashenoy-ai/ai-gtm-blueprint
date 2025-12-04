import streamlit as st
import pandas as pd
from openai import OpenAI
import random

# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(page_title="AI GTM Blueprint Generator", layout="wide")
st.title("🚀 AI GTM Blueprint Generator")
st.subheader("Generate GTM strategy based on real market signals (trending launches, sentiment, competitors)")

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ----------------------------
# Sample Trending Products (Simulated)
# ----------------------------
st.write("### 🔥 Trending Product Launches")
sample_products = pd.DataFrame({
    "Product": [
        "SmartSleep Tracker",
        "EcoWater Bottle",
        "AI Content Generator",
        "Fitness App Pro",
        "Plant-Based Protein"
    ],
    "Launch Date": [
        "2025-11-20", "2025-11-18", "2025-11-22", "2025-11-19", "2025-11-21"
    ],
    "Category": [
        "HealthTech", "Sustainability", "AI Tools", "Fitness", "Nutrition"
    ],
    "User Sentiment": [
        random.choice(["Positive", "Neutral", "Negative"]) for _ in range(5)
    ],
    "Competitors": [
        "CompA, CompB", "CompC", "CompD, CompE", "CompF", "CompG, CompH"
    ]
})
st.dataframe(sample_products)

# ----------------------------
# User Inputs
# ----------------------------
st.write("### ⚙️ Configure Analysis")
product_name = st.selectbox("Select product to analyze", sample_products["Product"])
include_competitors = st.checkbox("Include competitor mapping", value=True)
include_pricing = st.checkbox("Generate pricing & positioning insights", value=True)

# ----------------------------
# AI Analysis
# ----------------------------
if st.button("Generate GTM Blueprint"):
    with st.spinner("Generating AI GTM strategy..."):
        product_data = sample_products[sample_products["Product"] == product_name].to_dict(orient="records")[0]

        prompt = f"""
        You are a product strategist AI assistant.
        The product launch details are:
        {product_data}

        Tasks:
        1. Provide a GTM launch strategy.
        2. Suggest positioning and messaging.
        3. Recommend pricing insights.
        4. Map competitor moves if requested.
        5. Highlight risks and mitigation.
        Respond in markdown format with headings and bullet points.
        """

        if not include_competitors:
            prompt += "\nIgnore competitor mapping."

        if not include_pricing:
            prompt += "\nIgnore pricing insights."

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )

        st.markdown("### 📝 AI GTM Blueprint")
        st.markdown(response.choices[0].message.content)

# ----------------------------
# Footer
# ----------------------------
st.write("---")
st.write("💡 AI GTM Blueprint Generator | Powered by OpenAI | Sample data used for demo")
