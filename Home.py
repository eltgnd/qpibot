import time
import streamlit as st
import plotly.express as px
import pandas as pd
from grades import Grades
from streamlit_extras.add_vertical_space import add_vertical_space

# Settings
# st.set_page_config(layout='wide')

# Variables


# Functions
def error(message):
    st.write(message)
def save_edits():
    session_state.original_data = session_state.edited_data
def form_callable():
    try:
        df = get_table(session_state.str)
        session_state.original_data = df
    except:
        st.write('Error!')


# Header
st.title('🧮 QPI Wrapped')
add_vertical_space(1)
st.write('Inspired by CompSAt\'s QPI Calculator, QPI Wrapped calculates your QPI and visualizes your grades for fun! To get started, input your grades from AISIS. **Disclaimer: Your data is not saved.**')

# Tutorial
with st.expander('See how to copy paste grades', expanded=False):
    st.write('''1. Visit AISIS and go to `MY GRADES`.
        \n2. Select `ALL GRADES` from the dropdown and click the `DISPLAY GRADES` button.
        \n3. Copy the big table and paste it here!
    ''')
    st.image('https://scontent.xx.fbcdn.net/v/t1.15752-9/407088558_396969352731566_5235174993494823881_n.png?_nc_cat=103&ccb=1-7&_nc_sid=510075&_nc_eui2=AeEQIolU45pnuLrvVhT_5LSwec86j5goO6Z5zzqPmCg7phHZHCRq6OFBIoNhpqC9a8BaiRfCC9v85kGaHo8pE0rm&_nc_ohc=IstVxbAedXAAX8a7j5p&_nc_oc=AQl5EUZMveKZqWo7wmXntup_DCNDeTubAVcOc9HsZVOQ9HPt_LboQgk4DTkpOfE-w_No6XORLqAQycrq-ywacCBh&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.xx&cb_e2o_trans=q&oh=03_AdRg16NwA4mvNFXObHeOIn1vO_SxvkiwgnFMllnoYWvZdA&oe=65BCE003')

# if submit:
#     with st.form(key='df'):
#         df = get_table(s)
#         st.data_editor(df, hide_index=True, use_container_width=True)
#         update = st.form_submit_button(label='Update table')

# with open('sample_data.txt', 'r') as file:
#     s = file.read()

# Form
with st.form(key='form'):
    user_input = st.text_area('Input your grades from AISIS', key='str')
    submit = st.form_submit_button(label='Submit')

if submit:
    if 'data' not in st.session_state:
        st.session_state.data = user_input

try:
    s = st.session_state.data
    grades = Grades(s)

    # Wait
    add_vertical_space(1)
    with st.spinner('Analyzing your grades...'):
        time.sleep(3)
    st.toast('Done analyzing!', icon='🥳')

    # Table
    with st.expander('View Table', expanded=False):
        st.dataframe(grades.df, hide_index=True, use_container_width=True)

    # with st.sidebar:
    #     st.write('hi')
    #     # add search function for grade summary of specific coursecode (e.g. MATH)
    #     # add magna summa tool thingy
    #     # change color
    #     # 

    # Wait

    add_vertical_space(1)

    # Row 1
    width = [0.3,0.3,0.4] if grades.dean_list() else [0.5,0.5,0]
    col1, col2, col3 = st.columns(width)
    with col1:
        with st.container(border=True):
            cumulative_qpi_delta = round(grades.cumulative_qpi() - grades.cumulative_qpi_delta(), 2)
            st.metric(label="Cumulative QPI 🎯", value=grades.cumulative_qpi(), delta=f'{cumulative_qpi_delta} points')
    with col2:
        with st.container(border=True):
            latest_qpi_delta = round(grades.latest_qpi() - grades.latest_qpi_delta(), 2)
            st.metric(label='Semestral QPI 🪴', value=grades.latest_qpi(), delta=f'{latest_qpi_delta} points')
    with col3:
        if grades.dean_list():
            with st.container(border=True):
                st.metric(label='Dean\'s Lister Award 🎉', value=grades.dean_list(), delta='Congratulations!', delta_color='normal')

    add_vertical_space(1)

    # Row 2
    with st.container(border=True):
        option = st.toggle('Exclude Intersession QPI')
        fig = px.line(grades.qpi_by_semester(option), x='Semester', y='QPI', 
            title='QPI by Semester',
            markers=True,
            text='QPI',
            height=300)
        fig.update_traces(textposition="bottom left")
        fig.update_layout(margin=dict(l=30, r=30, t=50, b=20))
        st.plotly_chart(fig, use_container_width=True)

    add_vertical_space(1)

    # Row 3
    col1, col2 = st.columns([0.5,0.5])
    with col1:
        with st.container(border=True):
            pie, bar = st.tabs(['Pie Chart', 'Bar Chart'])
            with pie:
                if 'curr_sem1' not in st.session_state:
                    st.session_state.curr_sem1 = False
                fig = px.pie(grades.letter_frequency(st.session_state.curr_sem1), names='Final Grade', values='Subject Code',
                    title='Letter Grade Frequency',
                    height=380
                )
                fig.update_layout(legend=dict(
                    orientation='h',yanchor="top",y=0.1,xanchor="center",x=0.5),
                    margin=dict(l=20, r=20, t=30, b=0),
                    title=dict(x=0, y=0.95)
                )
                st.plotly_chart(fig, use_container_width=True)
                st.toggle('Current Semester Only', key='curr_sem1')
            with bar:
                if 'curr_sem2' not in st.session_state:
                    st.session_state.curr_sem2 = False
                fig = px.bar(grades.letter_frequency(st.session_state.curr_sem2), x='Final Grade', y='Subject Code',
                    title='Letter Grade Frequency',
                    height=380
                )
                fig.update_layout(legend=dict(
                    orientation='h',yanchor="top",y=0.9,xanchor="center",x=0.5),
                    margin=dict(l=20, r=20, t=50, b=0),
                    title=dict(x=0, y=0.95)
                )
                st.plotly_chart(fig, use_container_width=True)
                st.toggle('Current Semester Only', key='curr_sem2')

    with col2:
        with st.container(border=True):
            # Scale
            df = grades.qpi_by_course()
            df['Scaled'] = df[0]/4
            fig = px.line_polar(df, r='Scaled', theta='Course', 
                title='Overall Performance by Course',
                height=386,
                line_close=True)
            fig.update_polars(bgcolor='#0F1116', radialaxis=dict(visible=False, range=[0, 1]))
            fig.update_traces(fill='toself')
            fig.update_layout(margin=dict(l=35, r=35, t=50, b=20))
            st.plotly_chart(fig, use_container_width=True)

        with st.container(border=True):
            st.caption('**Disclaimer:** To avoid clutter, the radar chart above only includes courses with more than two subjects.')
    
    # Features list
    with st.expander('Features to implement soon', expanded=False):
        st.write('''
            1. Editable table
            2. Target cumulative QPI calculator
            3. Search function
            4. More insightful charts
        
        ''')
except:
    st.info('Waiting for input... 😴')