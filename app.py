st.markdown("---")
        st.markdown("### 🎯 Minimum Attendance Threshold & Top Performers")

        f_col1, f_col2, f_col3 = st.columns([2, 1.5, 1.5])
        min_threshold = f_col1.slider(
            "Minimum Required Attendance (%)",
            min_value=0,
            max_value=100,
            value=70,
            step=5
        )
        roster_scope = f_col2.selectbox(
            "Member Scope",
            ["Active Only", "All Roster (Incl. Inactive)"]
        )
        threshold_view = f_col3.selectbox(
            "Threshold View",
            ["All in Scope", "Below Minimum Only", "Meeting Minimum Only"]
        )

        scoped_df = active_summary_df.copy() if roster_scope == "Active Only" else summary_df.copy()
        scoped_df["Meets Target"] = scoped_df["Attendance Rate"] >= min_threshold

        meets_count = int(scoped_df["Meets Target"].sum())
        below_count = int((~scoped_df["Meets Target"]).sum())
        total_scoped = len(scoped_df)

        k1, k2, k3 = st.columns(3)
        k1.metric(f"Meeting ≥ {min_threshold}%", f"{meets_count} / {total_scoped}")
        k2.metric(f"Below {min_threshold}% Target", below_count)
        pass_pct = (meets_count / total_scoped * 100) if total_scoped > 0 else 0.0
        k3.metric("Compliance Rate", f"{pass_pct:.1f}%")

        if threshold_view == "Below Minimum Only":
            filtered_chart_df = scoped_df[~scoped_df["Meets Target"]].sort_values(by="Attendance Rate", ascending=True)
        elif threshold_view == "Meeting Minimum Only":
            filtered_chart_df = scoped_df[scoped_df["Meets Target"]].sort_values(by="Attendance Rate", ascending=False)
        else:
            filtered_chart_df = scoped_df.sort_values(by="Attendance Rate", ascending=False)

        left_vis, right_vis = st.columns([3, 2])

        with left_vis:
            st.markdown(f"#### 📊 Attendance vs. {min_threshold}% Minimum")
            if filtered_chart_df.empty:
                st.info("No members match the selected threshold filter.")
            else:
                chart_plot_df = filtered_chart_df.set_index("Player Name")[["Attendance Rate"]].copy()
                chart_plot_df["Target %"] = float(min_threshold)
                st.line_chart(chart_plot_df, height=320)

        with right_vis:
            st.markdown("#### 🏆 Top Performers Leaderboard")
            top_lb = active_summary_df.sort_values(
                by=["Attendance Rate", "Active Count", "Total Logged"],
                ascending=[False, False, False]
            ).head(10).copy()

            if top_lb.empty:
                st.info("No active member data to rank yet.")
            else:
                top_lb.insert(0, "Rank", range(1, len(top_lb) + 1))
                top_lb["Turnout"] = (top_lb["Active Count"] + top_lb["Zero Points Count"]).astype(str) + "/" + top_lb["Total Logged"].astype(str)
                top_lb["Rate"] = top_lb["Attendance Rate"].astype(str) + "%"
                st.dataframe(
                    top_lb[["Rank", "Player Name", "Rate", "Turnout", "Zero Points Count"]].rename(
                        columns={"Zero Points Count": "0-Pt"}
                    ),
                    use_container_width=True,
                    hide_index=True,
                    height=320
                )
