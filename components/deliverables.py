import streamlit as st


def render_table(df):

    st.subheader("📊 CL31 vs CL32 Comparison")

    col1, col2 = st.columns(2)

    with col1:
        status = st.multiselect(
            "Change Type",
            df["Change Type"].unique(),
            default=df["Change Type"].unique()
        )

    with col2:
        discipline = st.multiselect(
            "Discipline",
            df["Discipline"].unique(),
            default=df["Discipline"].unique()
        )

    filtered = df[
        (df["Change Type"].isin(status)) &
        (df["Discipline"].isin(discipline))
    ]

    st.dataframe(filtered, use_container_width=True)


# ----------------------------
# STRUCTURED VIEW (EXECUTIVE STYLE)
# ----------------------------
def render_structured_view(df):

    st.subheader("🧭 Structured Deliverables View")

    colour = {
        "NEW": "🟢",
        "REMOVED": "🔴",
        "DELAYED": "🟠",
        "UNCHANGED": "⚪"
    }

    for d in sorted(df["Discipline"].unique()):

        st.markdown(f"## 🏗 {d}")

        sub = df[df["Discipline"] == d]

        for t in ["DELAYED", "NEW", "REMOVED", "UNCHANGED"]:
            group = sub[sub["Change Type"] == t]

            if len(group) > 0:
                st.markdown(f"### {colour[t]} {t}")

                for _, r in group.iterrows():
                    st.markdown(
                        f"""
                        **{r['Deliverable']}**  
                        CL31: {r['CL31 Finish']} | CL32: {r['CL32 Finish']}  
                        Δ {r['Delta (Days)']} days  
                        _{r['Status / Comment']}_  
                        ---
                        """
                    )