import streamlit as st
import google.generativeai as genai

# ✅ Securely load Gemini API key from Streamlit Secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

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
Analyze the following resume line. Classify its quality as either 'Generic' or 'Impactful', and suggest a better version if needed.

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

Line: "{resume_line}"
Label:
"""

        try:
            # ✅ Correct model path required by Gemini
            model = genai.GenerativeModel(model_name="models/gemini-pro")
            chat = model.start_chat()
            response = chat.send_message(prompt)
            output = response.text.strip()

            # ✅ Display result
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
