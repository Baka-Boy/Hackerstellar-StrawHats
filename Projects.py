import streamlit as st
from streamlit_option_menu import option_menu

# Get the value of the "selected" query parameter
selected = st.experimental_get_query_params().get("selected", "Home")

# If "selected" is not present in the query parameters, assume that the user is on the home page
if selected == "Home":
    st.title("Home Page")
elif selected == "Projects":
    st.title("Projects Page")
    # Add content for the project page here
else:
    # If "selected" is present in the query parameters, display the appropriate content based on the selected option
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Projects", "Contact"],
        icons=["house", "book", "envelope"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )

    if selected == "Contact":
        st.title("Contact Page")
    else:
        # Set the "selected" query parameter to the selected option
        st.experimental_set_query_params(selected=selected)
