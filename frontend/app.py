import streamlit as st
import pandas as pd
from datetime import date

from add_update_ui import show_add_update_section
from analytics_ui import show_analytics_section

# ------------------------------------------------------------
# Basic configuration
# ------------------------------------------------------------
st.set_page_config(
    page_title="SpendWise – spend wisely and track your expenses",
    layout="wide",
    page_icon="💸",
)


#-----------------THEME------------------------
def inject_global_styles() -> None:
    """Inject CSS for permanent dark theme."""
    app_bg = "#020617"
    text_color = "#E5E7EB"
    subtext_color = "#9CA3AF"
    card_bg = "#0F172A"
    chip_bg = "#111827"
    chip_text = "#FBBF24"
    divider_grad = (
        "radial-gradient(circle at 0 0, rgba(148,163,184,0.45), transparent 60%),"
        "radial-gradient(circle at 100% 0, rgba(148,163,184,0.40), transparent 55%)"
    )

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {app_bg};
            color: {text_color};
        }}
        .main .block-container {{
            padding-top: 1.5rem;
            padding-bottom: 3rem;
        }}
        .main-title {{
            font-size: 2.8rem;
            font-weight: 800;
            line-height: 1.1;
            color: {text_color};
        }}
        .highlight {{
            color: #FF7A3C;
        }}
        .subheading {{
            font-size: 1rem;
            color: {subtext_color};
        }}
        .kudo-card {{
            background-color: {card_bg};
            padding: 1.2rem 1.8rem 1.6rem 1.8rem;
            border-radius: 1.5rem;
            box-shadow: 0 14px 35px rgba(15, 23, 42, 0.45);
        }}
        .kudo-chip {{
            display: inline-flex;
            align-items: center;
            padding: 0.15rem 0.7rem;
            border-radius: 999px;
            font-size: 0.8rem;
            font-weight: 500;
            background-color: {chip_bg};
            color: {chip_text};
        }}
        .nav-logo {{
            font-weight: 800;
            font-size: 1.1rem;
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            color: {text_color};
        }}
        .nav-menu {{
            text-align: center;
            color: {subtext_color};
            font-size: 0.95rem;
        }}
        .nav-menu span {{
            margin: 0 0.75rem;
            cursor: default;
        }}
        .hero-divider {{
            height: 24px;
            background: {divider_grad};
            -webkit-mask: url("data:image/svg+xml,%3Csvg width='1200' height='120' viewBox='0 0 1200 120' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0,0 C150,60 350,90 600,90 C850,90 1050,60 1200,0 L1200,120 L0,120 Z' fill='white'/%3E%3C/svg%3E") top left / cover no-repeat;
            mask: url("data:image/svg+xml,%3Csvg width='1200' height='120' viewBox='0 0 1200 120' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0,0 C150,60 350,90 600,90 C850,90 1050,60 1200,0 L1200,120 L0,120 Z' fill='white'/%3E%3C/svg%3E") top left / cover no-repeat;
            margin: 1.5rem 0 0.75rem 0;
        }}
        .section-title {{
            font-size: 1.6rem;
            font-weight: 700;
            color: {text_color};
        }}
        .section-subtitle {{
            font-size: 0.95rem;
            color: {subtext_color};
        }}
        .stButton>button {{
            border-radius: 999px;
            padding: 0.45rem 1.2rem;
            font-weight: 600;
            border: none;
        }}
        .stButton>button:hover {{
            opacity: 0.95;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# Layout helpers
# ------------------------------------------------------------
def render_navbar():
    """Top navigation bar — centered big SpendWise logo."""
    with st.container():
        # One centered column now
        col_center = st.columns([1])[0]

        with col_center:
            st.markdown(
                """
                <div style='text-align:center; margin-top: 10px;'>
                    <div class='nav-logo' style='font-size: 4rem;'>
                        💸 <span style='font-size: 4rem;'>SpendWise</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_hero():
    """Hero section inspired by Kudowall layout, center aligned."""
    with st.container():
        # Centered title
        st.markdown(
            "<div style='text-align:center;'>"
            "<div class='main-title'>People Trust "
            "<span class='highlight'>Numbers</span>. "
            "Turn Them Into Smarter Spending.</div>"
            "</div>",
            unsafe_allow_html=True,
        )

        st.write("")
        st.write("")
        st.write("")

        # Centered subtitle paragraph (this is the line you care about)
        st.markdown(
            "<p class='subheading' style='text-align:center; font-size:1.2rem;'>"
            "SpendWise helps you capture day-to-day expenses, see where your money goes, "
            "and stay on top of your budget — all in a few clicks."
            "</p>",
            unsafe_allow_html=True,
        )

        st.write("")
        st.write("")

        st.markdown("")

        # Center buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            pass
        with col2:
            col2a, col2b = st.columns([1, 1])
            with col2a:
                if st.button("Add an expense"):
                    st.session_state["main_view"] = "Add / Update"
            with col2b:
                if st.button("View analytics"):
                    st.session_state["main_view"] = "Analytics"
        with col3:
            pass

        st.write("")
        st.write("")

        st.markdown("")

        # Bullet points (use plain markdown, no HTML needed)
        st.markdown(
            "<div style='text-align:center;'>"
            "✅ See where your money goes each day  \n"
            "✅ Spot high-spend categories instantly  \n"
            "✅ Simple enough to keep using after day one"
            "</div>",
            unsafe_allow_html=True,
        )

    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")



# ------------------------------------------------------------
# Main app layout / router
# ------------------------------------------------------------
def main():

    inject_global_styles()
    render_navbar()
    render_hero()

    options = ["Add / Update", "Analytics"]
    if "main_view" not in st.session_state:
        st.session_state["main_view"] = "Add / Update"

    col_left, col_center, col_right = st.columns([1.1, 1, 0.7])
    with col_center:
        st.markdown(
            """
            <style>
            div.row-widget.stRadio > div {
                display: flex;
                justify-content: center;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        selected = st.radio(
            "Choose what you want to do today? ",
            options,
            horizontal=True,
            index=options.index(st.session_state["main_view"]),

        )

    st.session_state["main_view"] = selected

    st.markdown("")

    if selected == "Add / Update":
        show_add_update_section()
    else:
        show_analytics_section()


if __name__ == "__main__":
    main()
