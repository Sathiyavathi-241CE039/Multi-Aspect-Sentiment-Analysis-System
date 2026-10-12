            )


    # --------------------------------------------------------
    # PPT
    # --------------------------------------------------------

    with c2:

        st.markdown(
            """
            <div class="report-card">
                <h3>📊 PowerPoint Report</h3>
                <p>
                    Project presentation with analysis,
                    results and conclusions.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")


        if os.path.exists(ppt_path):

            with open(
                ppt_path,
                "rb"
            ) as file:

                st.download_button(
                    "⬇️ Download PowerPoint",
                    file,
                    file_name="sentiment_analysis_report.pptx",
                    mime=(
                        "application/vnd.openxmlformats-"
                        "officedocument.presentationml.presentation"
                    ),
                    use_container_width=True
                )

        else:

            st.warning(
                "PowerPoint report not found."
            )


    # --------------------------------------------------------
    # PROJECT OUTPUTS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '📌 Project Outputs'
        '</div>',
        unsafe_allow_html=True
    )


    o1, o2, o3 = st.columns(3)


    with o1:

        st.markdown(
            """
            <div class="insight-card">
                <div class="insight-title">
                    📊 Analytics
                </div>
                <div class="insight-value">
                    Sentiment Trends
                </div>
                <div class="kpi-small">
                    Monthly customer sentiment
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with o2:

        st.markdown(
            """
            <div class="insight-card">
                <div class="insight-title">
                    🎯 Aspect Analysis
                </div>
                <div class="insight-value">
                    10 Product Aspects
                </div>
                <div class="kpi-small">
                    Feature-level insights
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with o3:

        st.markdown(
            """
            <div class="insight-card">
                <div class="insight-title">
                    💡 Business Intelligence
                </div>
                <div class="insight-value">
                    Recommendations
                </div>
                <div class="kpi-small">
                    Actionable business insights
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown(
        '<div class="footer">'
        'Multi-Aspect Sentiment Analysis System'
