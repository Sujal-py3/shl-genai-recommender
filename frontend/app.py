import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="SHL Assessment Recommender", layout="centered")
st.title("🔍 SHL Assessment Recommender")
st.write("Enter a job description or query below to get the best assessment suggestions.")

query = st.text_area("Job Description or Query", height=150)

if st.button("Get Recommendations"):
    if not query.strip():
        st.warning("Please enter a job description or query.")
    else:
        with st.spinner("Querying backend..."):
            try:
                response = requests.post("https://shl-genai-recommender.onrender.com/recommend", json={"query": query})

                data = response.json()
                if response.status_code == 200 and len(data) > 0:
                    # Define desired columns
                    columns = [
                        "assessment_name",
                        "url",
                        "remote_testing",
                        "adaptive_support",
                        "duration",
                        "test_type",
                        "description"
                    ]
                    # Build dataframe with only selected columns
                    df = pd.DataFrame([{k: r.get(k, "") for k in columns} for r in data])
                    # Make assessment_name clickable
                    df["assessment_name"] = df.apply(
                        lambda row: f"[{row['assessment_name']}]({row['url']})", axis=1
                    )
                    df.drop("url", axis=1, inplace=True)
                    df.index += 1
                    st.success("Top Recommendations:")
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("No recommendations found.")
            except Exception as e:
                st.error(f"Error: {e}")
