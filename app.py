import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import plotly.express as px

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Placement Predictor", layout="wide")

# -----------------------------
# Title
# -----------------------------
st.title("🎓 Student Placement Predictor Dashboard")

# -----------------------------
# Load Data
# -----------------------------
train = pd.read_csv("train.csv")

# Show dataset
if st.checkbox("Show Dataset"):
    st.dataframe(train.head())

# -----------------------------
# Encoding
# -----------------------------
le = LabelEncoder()
for col in ['Gender','Degree','Branch','Placement_Status']:
    train[col] = le.fit_transform(train[col])

# -----------------------------
# Features & Model
# -----------------------------
X = train.drop(['Student_ID','Placement_Status'], axis=1)
y = train['Placement_Status']

model = RandomForestClassifier()
model.fit(X, y)

# -----------------------------
# SIDEBAR INPUT
# -----------------------------
st.sidebar.header("📥 Enter Student Details")

cgpa = st.sidebar.slider("CGPA", 0.0, 10.0, 7.0)
internships = st.sidebar.number_input("Internships", 0, 10, 1)
projects = st.sidebar.number_input("Projects", 0, 10, 2)
coding = st.sidebar.slider("Coding Skills", 0, 10, 5)
communication = st.sidebar.slider("Communication Skills", 0, 10, 5)
aptitude = st.sidebar.slider("Aptitude Score", 0, 100, 50)
certifications = st.sidebar.number_input("Certifications", 0, 10, 1)
backlogs = st.sidebar.number_input("Backlogs", 0, 10, 0)

# -----------------------------
# Prediction
# -----------------------------
if st.sidebar.button("Predict Placement"):
    input_data = np.array([[cgpa, internships, projects, coding,
                            communication, aptitude,
                            certifications, backlogs]])

    prediction = model.predict(input_data)

    if prediction[0] == 1:
        st.success("🎉 Student will be PLACED")
    else:
        st.error("❌ Student will NOT be placed")

# -----------------------------
# CGPA DISTRIBUTION
# -----------------------------
st.subheader("📊 CGPA Distribution Analysis")

st.markdown("""
**CGPA (Cumulative Grade Point Average)** represents academic performance.

Higher CGPA usually increases placement chances.
""")

fig = px.histogram(train, x="CGPA", color="Placement_Status", nbins=20)
st.plotly_chart(fig, use_container_width=True)

st.info("👉 Insight: Students with CGPA above ~7 have higher placement chances.")

# -----------------------------
# SKILLS ANALYSIS
# -----------------------------
st.subheader("📊 Skills Impact on Placement")

st.markdown("""
Coding Skills → Technical ability  
Communication Skills → Interview performance  

Both are equally important.
""")

fig = px.scatter(train,
                 x="Coding_Skills",
                 y="Communication_Skills",
                 size="CGPA",
                 color="Placement_Status")

st.plotly_chart(fig, use_container_width=True)

st.info("👉 Insight: Balanced skillset = higher placement success.")

# -----------------------------
# INTERNSHIP ANALYSIS
# -----------------------------
st.subheader("📊 Internship Impact")

st.markdown("""
Internships provide real-world experience and improve job readiness.
""")

fig = px.box(train,
             x="Placement_Status",
             y="Internships",
             color="Placement_Status")

st.plotly_chart(fig, use_container_width=True)

st.info("👉 Insight: More internships → better placement chances.")

# -----------------------------
# HEATMAP
# -----------------------------
st.subheader("📊 Correlation Heatmap")

st.markdown("""
Correlation shows relationship between variables.

+1 → Strong relation  
0 → No relation  
""")

corr = train.corr()

fig = px.imshow(corr, text_auto=True)
st.plotly_chart(fig, use_container_width=True)

st.info("👉 Insight: CGPA, skills and internships strongly influence placement.")

# -----------------------------
# PIE CHART
# -----------------------------
st.subheader("📊 Placement Distribution")

counts = train['Placement_Status'].value_counts()

fig = px.pie(names=["Not Placed", "Placed"],
             values=counts.values,
             hole=0.4)

st.plotly_chart(fig, use_container_width=True)

st.info("👉 Insight: Shows overall placement success ratio.")

# -----------------------------
# FEATURE IMPORTANCE
# -----------------------------
st.subheader("📊 Feature Importance")

importance = model.feature_importances_

imp_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": importance
}).sort_values(by="Importance", ascending=False)

fig = px.bar(imp_df, x="Feature", y="Importance")
st.plotly_chart(fig, use_container_width=True)

st.info("👉 Insight: Top features have highest impact on placement.")

# -----------------------------
# ANIMATION
# -----------------------------
st.subheader("🎬 Animated Placement Analysis")

fig = px.scatter(train,
                 x="CGPA",
                 y="Aptitude_Test_Score",
                 color="Placement_Status",
                 size="Coding_Skills",
                 animation_frame="Age")

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# FINAL CONCLUSION
# -----------------------------
st.subheader("🧠 Final Conclusion")

st.markdown("""
### 🔍 Key Insights:

- CGPA strongly affects placement  
- Coding + Communication skills are critical  
- Internships improve chances  
- Backlogs reduce success  

---

### 🎯 Final Thought:

Placement depends on a combination of:
- Academic performance  
- Skills  
- Experience  

👉 Balanced profile = highest success 🚀
""")
