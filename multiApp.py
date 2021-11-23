import streamlit as st

st.title("WEB APPLICATION FOR SENTIMENT ANALYSIS OF NETIZEN COMMENTS IN TWITTER ON PRIVATE UNIVERSITIES USING NAÏVE BAYES CLASSIFIER ALGORITHM")

class Multipage:
    """Framework for combining multiple streamlit applications"""

    def __init__(self) -> None:
        """Constructor class to generate a list which will store all our applications as an instance variable"""
        self.pages = []


    def add_page(self, title, func) -> None:
        """Class Method to Add pages to the project

        Args:
            title ([str]): The title of page which we are adding to the list of apps

            func: Python function to render this page in Streamlit
            """
        self.pages.append({
            "title": title,
            "function": func
        })

    def run(self):
        app = st.selectbox(
            'Menu',
            self.pages,
            format_func=lambda app: app['title'])

        app['function']()
        