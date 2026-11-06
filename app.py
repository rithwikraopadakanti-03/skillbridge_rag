import pandas as pd
import streamlit as st
import engine as E

st.set_page_config(page_title="SkillBridge Academic Insights", page_icon="🎓", layout="wide")

CODE_MAPS = {
    "Red=1": {1: "Red", 2: "Yellow", 3: "Orange", 4: "Green"},
    "On Track=1": {1: "On Track", 2: "Slightly Behind", 3: "Behind", 4: "At Risk"},
    "F=1": {1: "F", 2: "D", 3: "C", 4: "B", 5: "A", 6: "A+"},
    "Immediate=1": {1: "Immediate", 2: "High", 3: "Medium", 4: "Low"},
    "Yes=1": {1: "Yes", 0: "No"},
}
def decode(query, value):
    for key, m in CODE_MAPS.items():
        if key in query and int(round(value)) in m:
            return m[int(round(value))]
    return None

def show_result(query, res):
    if res is None:
        st.warning("No rule template matched this question.")
        return
    if res["answerable"] == 0:
        st.error("Out of scope: this can't be answered from the student data or policy documents.")
        st.caption("answerable=0, lookup_value=-1, rule_value=-1, final_answer=-1")
        return
    label = decode(query, res["final_answer"])
    c1, c2, c3 = st.columns(3)
    c1.metric("lookup_value", f"{res['lookup_value']:.2f}")
    c2.metric("rule_value", f"{res['rule_value']:.2f}")
    c3.metric("final_answer", f"{res['final_answer']:.2f}")
    if label: st.success(f"Answer: **{label}**")

st.sidebar.title("🎓 SkillBridge")
page = st.sidebar.radio("Page", ["Ask a question", "Student lookup", "Batch / course dashboard", "Run test set"])
st.sidebar.caption("Reference date: 2025-01-15")

if page == "Ask a question":
    st.title("Ask about student academics")
    examples = ["What is the overall grade of Arjun Singh (ID: STU0410)?",
                "What is the alert color for Ojasvi Rao (ID: STU0367)? (Red=1, Yellow=2, Orange=3, Green=4)",
                "What percentage of students in BATCH-2023-B have Green alert status?",
                "What is the CGPA of Soham Gupta in semester 1?"]
    ex = st.selectbox("Examples", [""] + examples)
    q = st.text_area("Your question", value=ex, height=90)
    if st.button("Answer", type="primary") and q.strip():
        show_result(q, E.solve(q))
    with st.expander("How lookup_value / rule_value work"):
        st.markdown("Plain lookups: `lookup = final`, `rule = 0`. Rule questions: `lookup` is the raw metric "
                    "(grade, attendance...), `rule` is the policy threshold or second metric, `final` is the result. "
                    "Group percentages: `lookup` = matching count, `rule` = group size.")

elif page == "Student lookup":
    st.title("Student lookup")
    opts = {f"{s} - {E.S.loc[s,'student_name']}": s for s in E.SIDS}
    sid = opts[st.selectbox("Student", list(opts))]
    m = E.student_metrics(sid)
    a, b, c, d = st.columns(4)
    a.metric("Grade", f"{m['grade']:.2f}", f"{m['grade']-m['passing_grade']:+.2f} vs pass")
    b.metric("Weighted attendance", f"{m['weighted_attendance']:.2f}%")
    c.metric("Alert", m["alert"])
    d.metric("Progress", m["progress"])
    st.write(f"**{m['name']}**, {m['course']}, {m['batch']}, mentor {m['mentor_id']}")
    comp = pd.DataFrame({"component": ["Quiz", "Assignment", "Project", "Exam"],
                         "average": [m["quiz_avg"], m["assignment_avg"], m["project_avg"], m["exam_avg"]]}).set_index("component")
    st.bar_chart(comp)
    st.dataframe(pd.DataFrame({"metric": list(m.keys()), "value": [f"{v:.2f}" if isinstance(v, float) else str(v) for v in m.values()]}), width="stretch", hide_index=True)

elif page == "Batch / course dashboard":
    st.title("Batch / course dashboard")
    c1, c2, c3 = st.columns(3)
    batch = c1.selectbox("Batch", ["All"] + sorted(E.S.batch.unique()))
    course = c2.selectbox("Course", ["All"] + sorted(E.S.course_name.unique()))
    dept = c3.selectbox("Mentor department", ["All"] + sorted(E.mentors.department.unique()))
    df = E.group_metrics(None if batch == "All" else batch, None if course == "All" else course,
                         None, None if dept == "All" else dept)
    if df.empty: st.info("No students match.")
    else:
        k = st.columns(4)
        k[0].metric("Students", len(df)); k[1].metric("Avg grade", f"{df.grade.mean():.2f}")
        k[2].metric("Avg weighted attendance", f"{df.weighted_attendance.mean():.2f}%")
        k[3].metric("Avg completion", f"{df.completion_pct.mean():.2f}%")
        l, r = st.columns(2)
        l.subheader("Alert distribution")
        l.bar_chart(df.alert.value_counts().reindex(["Red", "Yellow", "Orange", "Green"]).fillna(0))
        r.subheader("Progress status")
        r.bar_chart(df.progress.value_counts())
        st.dataframe(df[["student_id", "name", "batch", "course", "grade", "weighted_attendance", "alert", "progress"]]
                     .sort_values("grade"), width="stretch", hide_index=True)

else:
    st.title("Run query file")
    src = st.radio("Query set", ["test.csv (generate submission)", "train.csv (accuracy check)"], horizontal=True)
    if st.button("Run", type="primary"):
        qdf = E.test if src.startswith("test") else E.train
        rows = []
        for _, r in qdf.iterrows():
            p = E.solve(r["query"]) or E.OOS()
            rows.append({"query_id": r.query_id, "answerable": int(p["answerable"]),
                         "lookup_value": round(float(p["lookup_value"]), 2),
                         "rule_value": round(float(p["rule_value"]), 2),
                         "final_answer": round(float(p["final_answer"]), 2)})
        out = pd.DataFrame(rows)
        if src.startswith("train"):
            ok = sum(all(abs(out.loc[i, c] - qdf.loc[i, c]) <= 0.015 for c in out.columns[1:]) for i in out.index)
            st.metric("Rows matching ground truth", f"{ok}/{len(qdf)}")
        st.dataframe(out, width="stretch", hide_index=True)
        st.download_button("Download submission.csv", out.to_csv(index=False), "submission.csv", "text/csv")