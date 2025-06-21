import streamlit as st
import openai

# 🔐 Load OpenAI key from Streamlit Secrets Manager
openai.api_key = st.secrets["OPENAI_API_KEY"]

# 🌐 Page setup
st.set_page_config(page_title="Resume Line Quality Checker", layout="centered")
st.title("📋 Resume Line Quality Checker")
st.subheader("🧠 Classify and Improve Your Resume Bullets Using AI")

# 📝 User input
resume_line = st.text_area("✍️ Paste a resume line, summary, or bullet point:")

# 🔁 On submit
if st.button("Check Quality"):
    if resume_line.strip() == "":
        st.warning("Please enter a line to analyze.")
    else:
        # 🎯 Few-shot prompt
        prompt = f"""
Analyze the following resume line. Classify its quality, and suggest a better version if needed.

Examples:

Line: "Led team meetings every week."
Label: Generic
Suggested Rewrite: "Facilitated weekly team meetings to align goals and drive cross-functional collaboration."

Line: "Increased website traffic by 40% through SEO optimization."
Label: Impactful
Suggested Rewrite: -

Line: "Worked in marketing department."
Label: Generic
Suggested Rewrite: "Assisted in executing 5 product campaigns, contributing to a 12% increase in lead generation."

Line: "Managed $500K budget and reduced operational costs by 15%."
Label: Impactful
Suggested Rewrite: -

Line: "Led team meetings every week."
Label: Generic
Suggested Rewrite: "Facilitated weekly team meetings to align goals and drive cross-functional collaboration."

Line: "Increased website traffic by 40% through SEO optimization."
Label: Impactful
Suggested Rewrite: –

Line: "Worked in marketing department."
Label: Generic
Suggested Rewrite: "Assisted in executing 5 product campaigns, contributing to a 12% increase in lead generation."

Line: "Managed $500K budget and reduced operational costs by 15%."
Label: Impactful
Suggested Rewrite: –

Additional Examples in Your Format
Line: "Handled customer inquiries."
Label: Generic
Suggested Rewrite: "Resolved 50+ customer inquiries daily with a 98% satisfaction rate, reducing escalations by 25%."

Line: "Optimized supply chain logistics, cutting delivery times by 20%."
Label: Impactful
Suggested Rewrite: –

Line: "Wrote code for software features."
Label: Generic
Suggested Rewrite: "Developed 3 scalable API integrations, improving system efficiency by 35%."

Line: "Boosted sales revenue by $1.2M in Q3 through strategic partnerships."
Label: Impactful
Suggested Rewrite: –

Line: "Created content for social media platforms daily."
Label: Generic
Suggested Rewrite: "Developed and posted daily social media content, growing follower engagement by 25% across Instagram and LinkedIn."

Line: "Drove a paid ad campaign that boosted conversions by 35% with a $50K budget."
Label: Impactful
Suggested Rewrite: -

Line: "Helped with marketing tasks and supported team goals."
Label: Generic
Suggested Rewrite: "Supported 3 major marketing initiatives, increasing brand visibility by 10% through targeted email campaigns."

Line: "{resume_line}"
Label:
"""

        # 🧠 Call OpenAI
        try:
            response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that analyzes resume lines."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.7,
    max_tokens=150
)

output = response.choices[0].message.content.strip()

            # 🖥️ Display results
            st.markdown("### 🔍 Classification & Rewrite Suggestion")
            if "Suggested Rewrite:" in output:
                parts = output.split("Suggested Rewrite:")
                st.markdown(f"**🔖 Classification:** `{parts[0].replace('Label:', '').strip()}`")
                suggestion = parts[1].strip()
                if suggestion != "-" and suggestion != "":
                    st.markdown("**✏️ Suggested Rewrite:**")
                    st.success(suggestion)
                else:
                    st.info("✅ No rewrite needed — this line is already impactful!")
            else:
                st.write(output)

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")
