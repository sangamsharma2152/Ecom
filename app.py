import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import plotly.express as px

# -----------------------------
# PAGE CONFIG + UI STYLE
# -----------------------------
st.set_page_config(page_title="Placement Predictor", layout="wide")

# Animated background
st.markdown("""
<style>
@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
.stApp {
    background: linear-gradient(-45deg, #1e3c72, #2a5298, #6a11cb, #2575fc);
    background-size: 400% 400%;
    animation: gradientBG 10s ease infinite;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("🎓 AI-Based Student Placement Advisor")

# -----------------------------
# LOAD DATA
# -----------------------------
train = pd.read_csv("train.csv")

if st.checkbox("Show Dataset"):
    st.dataframe(train.head())

# -----------------------------
# ENCODING
# -----------------------------
le = LabelEncoder()

categorical_cols = ['Gender', 'Degree', 'Branch', 'Placement_Status']
for col in categorical_cols:
    if col in train.columns:
        train[col] = le.fit_transform(train[col])

# -----------------------------
# MODEL TRAINING
# -----------------------------
X = train.drop(['Student_ID','Placement_Status'], axis=1)
y = train['Placement_Status']

model = RandomForestClassifier()
model.fit(X, y)

# -----------------------------
# USER INPUT (DYNAMIC)
# -----------------------------
st.sidebar.header("📥 Enter Student Details")

input_dict = {}

for col in X.columns:
    if col == "CGPA":
        input_dict[col] = st.sidebar.slider("CGPA", 0.0, 10.0, 7.0)

    elif col in ["Internships", "Projects", "Certifications", "Backlogs"]:
        input_dict[col] = st.sidebar.number_input(col, 0, 10, 1)

    elif col in ["Coding_Skills", "Communication_Skills"]:
        input_dict[col] = st.sidebar.slider(col, 0, 10, 5)

    elif col == "Aptitude_Test_Score":
        input_dict[col] = st.sidebar.slider("Aptitude Score", 0, 100, 50)

    else:
        input_dict[col] = st.sidebar.number_input(col, 0, 100, 0)

# -----------------------------
# PREDICTION + SUGGESTIONS
# -----------------------------
if st.sidebar.button("Predict Placement"):

    input_df = pd.DataFrame([input_dict])
    input_df = input_df[X.columns]

    prediction = model.predict(input_df)

    if prediction[0] == 1:
        st.success("🎉 Student will be PLACED")
    else:
        st.error("❌ Student will NOT be placed")

    # -----------------------------
    # AI SUGGESTIONS
    # -----------------------------
    st.subheader("🧠 Personalized Improvement Suggestions")

    suggestions = []

    if input_dict.get("CGPA", 0) < 7:
        suggestions.append("📈 Improve CGPA (target above 7)")

    if input_dict.get("Coding_Skills", 0) < 6:
        suggestions.append("💻 Improve coding skills (DSA + projects)")

    if input_dict.get("Communication_Skills", 0) < 6:
        suggestions.append("🗣 Work on communication (mock interviews)")

    if input_dict.get("Internships", 0) < 2:
        suggestions.append("🏢 Do more internships")

    if input_dict.get("Projects", 0) < 2:
        suggestions.append("📂 Build more projects")

    if input_dict.get("Certifications", 0) < 2:
        suggestions.append("📜 Add certifications")

    if input_dict.get("Backlogs", 0) > 0:
        suggestions.append("❌ Clear backlogs")

    if suggestions:
        for s in suggestions:
            st.warning(s)
    else:
        st.success("🔥 Excellent profile!")

    # -----------------------------
    # FINAL EVALUATION
    # -----------------------------
    st.subheader("🎯 Final Evaluation")

    if prediction[0] == 1:
        st.info("You are on the right track. Keep improving!")
    else:
        st.info("Focus on the above areas to improve placement chances.")

# -----------------------------
# VISUALIZATIONS
# -----------------------------

st.subheader("📊 CGPA Distribution")
fig1 = px.histogram(train, x="CGPA", color="Placement_Status", nbins=20)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("📊 Skills Analysis")
fig2 = px.scatter(train,
                  x="Coding_Skills",
                  y="Communication_Skills",
                  size="CGPA",
                  color="Placement_Status")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("📊 Internship Impact")
fig3 = px.box(train,
              x="Placement_Status",
              y="Internships",
              color="Placement_Status")
st.plotly_chart(fig3, use_container_width=True)

st.subheader("📊 Heatmap")
corr = train.corr()
fig4 = px.imshow(corr, text_auto=True)
st.plotly_chart(fig4, use_container_width=True)

st.subheader("📊 Placement Distribution")
counts = train['Placement_Status'].value_counts()
fig5 = px.pie(names=["Not Placed", "Placed"],
              values=counts.values,
              hole=0.4)
st.plotly_chart(fig5, use_container_width=True)

st.subheader("📊 Feature Importance")
importance = model.feature_importances_
imp_df = pd.DataFrame({"Feature": X.columns, "Importance": importance})
fig6 = px.bar(imp_df, x="Feature", y="Importance")
st.plotly_chart(fig6, use_container_width=True)

st.subheader("🎬 Animated Trend")
fig7 = px.scatter(train,
                  x="CGPA",
                  y="Aptitude_Test_Score",
                  color="Placement_Status",
                  size="Coding_Skills",
                  animation_frame="Age")
st.plotly_chart(fig7, use_container_width=True)

# -----------------------------
# FINAL INSIGHT
# -----------------------------
st.subheader("🧠 Conclusion")

st.markdown("""
- CGPA, skills, and internships are key factors  
- Backlogs negatively affect placement  
- Balanced profile leads to success  

👉 This system not only predicts but guides improvement.
""")
