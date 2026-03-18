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
# Features & Target
# -----------------------------
X = train.drop(['Student_ID','Placement_Status'], axis=1)
y = train['Placement_Status']

# -----------------------------
# Train Model
# -----------------------------
model = RandomForestClassifier()
model.fit(X, y)

# -----------------------------
# Sidebar Input
# -----------------------------
st.sidebar.header("Enter Student Details")

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
# 📊 MAIN VISUALS
# -----------------------------
st.subheader("📊 CGPA vs Aptitude Analysis")

fig1 = px.scatter(
    train,
    x="CGPA",
    y="Aptitude_Test_Score",
    color="Placement_Status",
    size="Coding_Skills",
    animation_frame="Age",
    title="Placement Analysis"
)

st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# 📊 Feature Importance
# -----------------------------
st.subheader("📊 Feature Importance")

importance = model.feature_importances_

imp_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": importance
}).sort_values(by="Importance", ascending=False)

fig2 = px.bar(
    imp_df,
    x="Feature",
    y="Importance",
    title="Factors Affecting Placement"
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# 📊 Heatmap
# -----------------------------
st.subheader("📊 Correlation Heatmap")

corr = train.corr()

fig_heat = px.imshow(
    corr,
    text_auto=True,
    title="Feature Correlation"
)

st.plotly_chart(fig_heat, use_container_width=True)

# -----------------------------
# 📊 Placement Distribution
# -----------------------------
st.subheader("📊 Placement Distribution")

fig3 = px.pie(
    train,
    names="Placement_Status",
    title="Placed vs Not Placed"
)

st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# 📊 CGPA Distribution
# -----------------------------
st.subheader("📊 CGPA Distribution")

fig4 = px.histogram(
    train,
    x="CGPA",
    color="Placement_Status",
    nbins=20,
    title="CGPA Distribution"
)

st.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# 📊 Skills Bubble Chart
# -----------------------------
st.subheader("📊 Skills Impact")

fig5 = px.scatter(
    train,
    x="Coding_Skills",
    y="Communication_Skills",
    size="CGPA",
    color="Placement_Status",
    title="Skills vs Placement"
)

st.plotly_chart(fig5, use_container_width=True)

# -----------------------------
# 📊 Internships Analysis
# -----------------------------
st.subheader("📊 Internships Impact")

fig6 = px.box(
    train,
    x="Placement_Status",
    y="Internships",
    title="Internships vs Placement"
)

st.plotly_chart(fig6, use_container_width=True)

# -----------------------------
# 🎬 Animated Trend
# -----------------------------
st.subheader("🎬 Animated Placement Trend")

fig7 = px.scatter(
    train,
    x="CGPA",
    y="Aptitude_Test_Score",
    color="Placement_Status",
    size="Coding_Skills",
    animation_frame="Age",
    title="Dynamic Placement Visualization"
)

st.plotly_chart(fig7, use_container_width=True)

# -----------------------------
# 🧠 Insights Section
# -----------------------------
st.subheader("🧠 Key Insights & Conclusions")

st.markdown("""
### 🔍 Key Findings:

- Higher **CGPA → Higher placement chances**
- **Coding + Communication skills** are critical
- **Internships & Projects boost placement**
- **Backlogs reduce chances significantly**
- Skills combination matters more than a single factor

### 🎯 Final Conclusion:

Placement depends on:
- Academic performance (CGPA)
- Practical exposure (Internships, Projects)
- Technical + soft skills

👉 Students who improve all these areas have the highest success rate.
""")
