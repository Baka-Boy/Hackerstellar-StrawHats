import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide", page_icon=":money_with_wings:")

selected = option_menu(
    menu_title="Main Menu",
    options=["Expense Tracker", "AI Chatbot"],
    icons=["house", "book", "envolope"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)


if selected == "Expense Tracker":
    #imports for our app
    import streamlit as st
    import plotly.graph_objects as go
    from streamlit_option_menu import option_menu
    import pandas as pd

    import calendar
    from datetime import datetime


    df = pd.read_csv(r'./spending.csv')
    #variables
    # incomes = ["Salary","Blog","Other Income"]
    # expenses = ["Amount"]
    # Category=["Category"]
    # Description=["Description"]
    currency = "Rs"
    page_title = "Expense Stream"
    page_icon = ":money_with_wings:"
    layout = "centered"


    today = datetime.today()

    # def get_all_periods():
    #     items = db.fetch_all_periods()
    #     periods = [item["key"] for item in items]
    #     return periods

    hide_st_style = """
    <style>
    #MainMenu {visiblility: hidden;}
    footer {visiblility: hidden;}
    header {visiblility: hidden;}
    </style>
    """

    st.markdown(hide_st_style,unsafe_allow_html=True)

    selected = option_menu(
        menu_title= None,
        options=["Data Entry","Data Visualization"],
        icons=["pencil-fill","bar-chart-fill"],
        orientation= "horizontal",
    )


    if selected == "Data Entry":
            st.header(f"Data Entry in {currency}")
            with st.form("Entry_form", clear_on_submit=True):

                # with st.expander("Income"):
                #     for income in incomes:
                #         st.number_input(f"{income}:",min_value=0, format="%i", step=10,key=income)
                # with st.expander("Expenses"):
                #     for expense in expenses:
                #         st.number_input(f"{expense}:", min_value=0,format="%i",step=10,key=expense)
                # with st.expander("Category"):
                #     Category = st.text_area("", placeholder="Enter Category hee ...")
                # with st.expander("Description"):
                #     Description = st.text_area("", placeholder="Enter Description hee ...")

                Date=st.text_input("Date")
                Category=st.text_input("Category")
                Amount=st.text_input("Amount")
                Description=st.text_input("Description")



                submitted = st.form_submit_button("Submit")
                if submitted:
                    st.write(Date,Category,Amount,Description)
                    new_data = {"date": Date, "category":Category, "amount":Amount, "description":Description}
                    df=df.append(new_data, ignore_index=True)
                    df.to_csv(r'./spending.csv', index=False)
                    st.success("Data Saved!")


    if selected == "Data Visualization":
        st.header("Data Visualization")
        csv_file = st.file_uploader("Upload CSV", type=["csv"])

        if csv_file is not None:
            # Load CSV data into a pandas dataframe
            df = pd.read_csv(csv_file)
            
            # Display dataframe in Streamlit
            st.write(df)
            
            with st.form("Visualization_form", clear_on_submit=True):
                submitted = st.form_submit_button("Submit")
                if submitted:
                    st.success("File Uploaded Successfully!")

            # Move download button outside of form block
            Visualization = open(r"./Visualization.pdf", "rb").read()
            st.download_button(label="Download file", data=Visualization, file_name="Visualization.pdf", mime="pdf")



    

if selected == "AI Chatbot":
    import os
    import nltk
    import ssl
    import streamlit as st
    import random
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression

    ssl._create_default_https_context = ssl._create_unverified_context
    nltk.data.path.append(os.path.abspath("nltk_data"))
    nltk.download('punkt')

    intents =   [
                {
                    "tag": "greeting",
                    "patterns": ["Hi", "Hello", "Hey", "How are you", "What's up"],
                    "responses": ["Hi there", "Hello", "Hey", "I'm fine, thank you", "Nothing much"]
                },
                {
                    "tag": "goodbye",
                    "patterns": ["Bye", "See you later", "Goodbye", "Take care"],
                    "responses": ["Goodbye", "See you later", "Take care"]
                },
                {
                    "tag": "thanks",
                    "patterns": ["Thank you", "Thanks", "Thanks a lot", "I appreciate it"],
                    "responses": ["You're welcome", "No problem", "Glad I could help"]
                },
                {
                    "tag": "about",
                    "patterns": ["What can you do", "Who are you", "What are you", "What is your purpose"],
                    "responses": ["I am a chatbot", "My purpose is to assist you", "I can answer questions and provide assistance"]
                },
                {
                    "tag": "help",
                    "patterns": ["Help", "I need help", "Can you help me", "What should I do"],
                    "responses": ["Sure, what do you need help with?", "I'm here to help. What's the problem?", "How can I assist you?"]
                },
                {
                    "tag": "Sustainable behavior",
                    "patterns": ["How can I promote sustainable behavior on Terra Nova?",
                                "What are some examples of sustainable practices on the planet?",
                                "What are the benefits of sustainable behavior on Terra Nova?"],
                    "responses": ["You can reduce your energy consumption on Terra Nova by using energy-efficient appliances and devices, turning off lights and electronics when not in use, and using renewable energy sources like solar power or wind power.", "Some sustainable solutions for transportation on Terra Nova include using electric or hybrid vehicles, carpooling or using public transportation, and biking or walking whenever possible."]
                },
                {
                    "tag": "Expense monitoring",
                    "patterns": ["How can I track my expenses effectively on Terra Nova?",
                                "What are some common expenses to watch out for on the planet?",
                                "What are some sustainable solutions for transportation on Terra Nova?",
                                "How can I reduce my expenses on Terra Nova?"],
                    "responses": ["To track your expenses effectively on Terra Nova, consider using a budgeting app or spreadsheet. Make sure to record all of your expenses, including small purchases such as coffee or snacks. This will help you identify areas where you can cut back and save money.",
                                "Common expenses to watch out for on Terra Nova include transportation, food, and housing. Make sure to research your options carefully and compare prices before making any major purchases or commitments.",
                                "What are some sustainable solutions for transportation on Terra Nova?","One way to reduce your expenses on Terra Nova is to share resources with other colonizers. For example, you can carpool to work or share a garden plot to grow food. You can also consider living in a smaller or more energy-efficient home to save on housing costs."]
                },
                
                {
                    "tag": "investing",
                    "patterns": [
                        "What are the best ways to invest my money?",
                        "How can I start investing?",
                        "What is a stock market?",
                        "how to invest?",
                        "investment plans",
                        "What financial planning tools are available on Terra Nova?",
                        "How can I use technology to manage my finances on the planet?",
                        "What are some benefits of using financial planning tools on Terra Nova?"

                    ],
                    "responses": [
                        "The best way to invest your money depends on your financial goals and risk tolerance. Some popular investment options include stocks, bonds, mutual funds, and real estate. Before making any investments, it's important to do your research and consult with a financial advisor to determine what strategy is best for you.",
                        "You can start investing by opening a brokerage account with a reputable online broker. Then, you can start investing in stocks, bonds, or mutual funds that align with your investment goals.",
                        "The stock market is a place where publicly-traded companies' stocks are bought and sold. It can be a way for investors to earn returns on their investment by buying stocks that increase in value over time.",
                        "There are many financial planning tools available on Terra Nova, including budgeting apps, investment calculators, and retirement planning tools. Make sure to research your options carefully and choose tools that meet your specific needs and goals.",
                        "One way to use technology to manage your finances on Terra Nova is to set up automatic payments and transfers. This can help you avoid late fees and penalties, and ensure that you stay on track with your financial goals.",
                        "Benefits of using financial planning tools on Terra Nova include better visibility and control over your finances, increased efficiency and accuracy in tracking expenses and investments, and the ability to make more informed decisions about your money."
                    ]
                },
                
                {
                    "tag": "retirement",
                    "patterns": [
                        "What is a 401(k)?",
                        "How can I start saving for retirement?",
                        "retirement",
                        "retirement on Terra Nova",
                        "retirement options",
                        "retirement plans",
                        "What is the best retirement plan for me?"
                    ],
                    "responses": [
                        "A 401(k) is a retirement savings plan offered by employers. With a 401(k), you can contribute a portion of your pre-tax income to a retirement account, which can grow tax-free until retirement. Many employers also offer matching contributions, which can help your savings grow even faster.",
                        "You can start saving for retirement by opening an Individual Retirement Account (IRA) or by participating in a 401(k) or other employer-sponsored retirement plan. You can also explore other retirement savings options, such as annuities or real estate investments. The best retirement plan for you depends on your individual financial situation and goals, so it's important to do your research and consult with a financial advisor to determine what strategy is best for you."
                    ]
                },
                {
                    "tag": "taxes",
                    "patterns": [
                    "What are some tax deductions I can claim?",
                    "When is the tax filing deadline?",
                    "taxes",
                    "tax reduction",
                    "How can I reduce my tax bill?"
                    ],
                    "responses": [
                    "There are many tax deductions you may be able to claim, including deductions for charitable contributions, medical expenses, and business expenses. It's important to consult with a tax professional to determine what deductions you qualify for.",
                    "The tax filing deadline is usually April 15th, but it can vary depending on the year and your individual tax situation. It's important to check with the IRS or a tax professional to make sure you file on time.",
                    "There are several ways to reduce your tax bill, such as contributing to a retirement account, taking advantage of tax deductions, and exploring tax credits. Again, it's important to consult with a tax professional to determine what strategies are best for your individual situation."
                    ]
                },
                {
                    "tag": "budget",
                    "patterns": ["How can I make a budget", "What's a good budgeting strategy", "How do I create a budget","How can I save money?",
                        "What are some budgeting strategies?","make budget","budget","What are some tips for sticking to a budget on Terra Nova?",
                        "How can I save money while still enjoying my life on Terra Nova?",
                        "What are some common budgeting mistakes to avoid?",
                        "How do I create a budget?"],
                            "responses": [ "There are many ways to save money. One effective strategy is to create a budget that outlines your monthly income and expenses. This can help you identify areas where you can reduce unnecessary spending. Another option is to find ways to increase your income, such as taking on a side hustle or negotiating a raise at work.",
                                "A good budgeting strategy is to use the 50/30/20 rule. This means allocating 50% of your income towards essential expenses, 30% towards discretionary expenses, and 20% towards savings and debt repayment.",
                                "To create a budget, start by setting financial goals for yourself. Then, track your income and expenses for a few months to get a sense of where your money is going. Next, create a budget by allocating your income towards essential expenses, savings and debt repayment, and discretionary expenses.",
                        "To make a budget, start by tracking your income and expenses. Then, allocate your income towards essential expenses like rent, food, and bills. Next, allocate some of your income towards savings and debt repayment. Finally, allocate the remainder of your income towards discretionary expenses like entertainment and hobbies.", "A good budgeting strategy is to use the 50/30/20 rule. This means allocating 50% of your income towards essential expenses, 30% towards discretionary expenses, and 20% towards savings and debt repayment.", "To create a budget, start by setting financial goals for yourself. Then, track your income and expenses for a few months to get a sense of where your money is going. Next, create a budget by allocating your income towards essential expenses, savings and debt repayment, and discretionary expenses.",
                        "One tip for sticking to a budget on Terra Nova is to focus on experiences rather than material possessions. There are many free or low-cost activities to enjoy on the planet, such as hiking or stargazing. You can also save money by growing your own food or shopping at local markets.",
                    "Another way to save money on Terra Nova is to be mindful of your energy usage. Make sure to turn off lights and appliances when not in use, and consider investing in renewable energy sources such as solar or wind power.",
                    "Common budgeting mistakes to avoid on Terra Nova include overspending on luxury items, underestimating expenses such as medical costs, and failing to plan for emergencies or unexpected events."]
                },
                {
                    "tag": "credit_score",
                    "patterns": ["What is a credit score", "How do I check my credit score", "How can I improve my credit score","What is a credit score?","credit score",
                        "How do I check my credit score?",
                        "How can I improve my credit score?"],
                    "responses": ["A credit score is a number that represents your creditworthiness. It is based on your credit history and is used by lenders to determine whether or not to lend you money. The higher your credit score, the more likely you are to be approved for credit.",
                        "You can check your credit score for free on several websites such as Credit Karma and Credit Sesame.",
                        "Improving your credit score takes time and effort. One key strategy is to make sure you're paying all of your bills on time, as late payments can negatively impact your credit score. Additionally, reducing your debt and avoiding opening too many new credit accounts at once can also help boost your score."
                    ,"A credit score is a number that represents your creditworthiness. It is based on your credit history and is used by lenders to determine whether or not to lend you money. The higher your credit score, the more likely you are to be approved for credit.", "You can check your credit score for free on several websites such as Credit Karma and Credit Sesame."]
                }
                ]

    # Create the vectorizer and classifier
    vectorizer = TfidfVectorizer()
    clf = LogisticRegression(random_state=0, max_iter=10000)

    # Preprocess the data
    tags = []
    patterns = []
    for intent in intents:
        for pattern in intent['patterns']:
            tags.append(intent['tag'])
            patterns.append(pattern)

    # training the model
    x = vectorizer.fit_transform(patterns)
    y = tags
    clf.fit(x, y)

    def chatbot(input_text):
        input_text = vectorizer.transform([input_text])
        tag = clf.predict(input_text)[0]
        for intent in intents:
            if intent['tag'] == tag:
                response = random.choice(intent['responses'])
                return response
            

    counter = 0

    def main():
        global counter
        st.title("Chatbot")
        st.write("Welcome to the chatbot. Please type a message and press Enter to start the conversation.")

        counter += 1
        user_input = st.text_input("You:", key=f"user_input_{counter}")

        if user_input:
            response = chatbot(user_input)
            st.text_area("Chatbot:", value=response, height=100, max_chars=None, key=f"chatbot_response_{counter}")

            if response.lower() in ['goodbye', 'bye']:
                st.write("Thank you for chatting with me. Have a great day!")
                st.stop()

    if __name__ == '__main__':
        main()