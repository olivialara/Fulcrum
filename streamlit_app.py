import streamlit as st
import pandas as pd
import numpy as np
#plotly imports
import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import json
import openai

st.title("Fulcrum Case Study")
# st.header("Search By Punk ID")
st.subheader("AI Chatbot: Policy Proposal Help")
st.write("[Fulcrum](https://www.withfulcrum.com/) gives AI-Powered products to insurance brokerages. They give clients \
          the ability ask questions on generated and active policies. Inspired by such work, I have created a simple chatbot \
         built to help users understand commercial policy proposals and ask questions on it.")

# # Initialize chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Display chat messages from history on app rerun
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # React to user input
# if prompt := st.chat_input("What is up?"):
#     # Display user message in chat message container
#     st.chat_message("user").markdown(prompt)
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": prompt})

#     response = f"Echo: {prompt}"
#     # Display assistant response in chat message container
#     with st.chat_message("assistant"):
#         st.markdown(response)
#     # Add assistant response to chat history
#     st.session_state.messages.append({"role": "assistant", "content": response})

openai.api_key = st.secrets["OPENAI_API_KEY"]

# User input
user_input = st.text_area("Enter your message:", "")

if st.button("Send"):
    if user_input:
        with st.spinner("Generating response..."):
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo",  # Replace with your custom GPT's model name if different
                messages=[{"role": "user", "content": user_input}],
            )
            st.write("### Response:")
            st.write(response["choices"][0]["message"]["content"])
    else:
        st.warning("Please enter a message.")
         

st.subheader("Policy Data Visualizations: POMS")
st.write("Another feature Fulcrum offers \
         is the ability to summarize active policies for their accounts. In this case study, \
         I created some policy data visualizations for one of Fulcrum's current clinets, [POMS](https://www.pomsassoc.com/). \
         The data used to generate these visualizations are completely random and only \
         used for visualization purposes.")

#image = Image.open('images/cryptopunks-image.jpg')

def graph_policy_breakdown_by_insurance_type():
    data = {'Insurance Type': ['Commercial', 'Auto', 'Home', 'Life'],
            'Percentage': [.59, .22, .15, .04],
            'Format': ['59%', '22%', '15%', '4%'],
            'Count': [1475, 550, 375, 100]
        }
    df = pd.DataFrame(data)

    fig = px.bar(df, 
             x= "Insurance Type",
             y= "Count",
             text = 'Format',
             color_discrete_sequence = ['#056374']
            )
            
    fig.update_layout(title = 'Policy Breakdown', height=400)

    fig.update_traces(
    hovertemplate='<b>Insurance Type: %{x}</b><br>Count: %{y}<br>Percentage: %{text}'
    )

    return fig

def graph_monthly_trends():
    data = {'Date': ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 
                           'Aug', 'Sep', 'Oct',
                           'Nov', 'Dec'],
        'Format': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        '2024': [145, 204, 336, 207, 159, 97, 72, 85, 96, 150, 170, 112],
        '2023': [101, 188, 207, 156, 105, 35, 90, 77, 101, 119, 101, 80]
       }

    df = pd.DataFrame(data)
    fig = go.Figure()

    fig.add_trace(
    go.Scatter(
        x=df['Date'],
        y=df['2023'],
        marker = {'color': '#dc3828'},
        name="Prev. Year" 
    ))

    fig.add_trace(
    go.Bar(
        x=df['Date'],
        y=df['2024'],
        marker = {'color': '#056374'},
        name="2024" 
    ))

    fig.update_layout(title = 'Monthly Trends', 
                  #title_x=.5, 
                  xaxis_title="Month", 
                  yaxis_title="New Policies Generated",
                  hovermode='x unified',
                  height=400
                 )
    return fig

def graph_policy_breakdown_by_state():
    pio.templates.default = "plotly_dark"
    states = pd.read_csv('insurance-policy-count-by-state.csv') 
    code = {'Alabama': 'AL',
        'Alaska': 'AK',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'District of Columbia': 'DC',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virginia': 'VA',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY'}
    states['Code'] = states['State'].map(code)

    fig = px.choropleth(states,
        locations='Code',
        color='2024',
        color_continuous_scale='bluyl',
        hover_name='State',
        locationmode='USA-states',
        hover_data=["2024"],
        labels={'2024':'Count', 'Code': 'Abbv.'},
        scope='usa',
        height=800,
        width=1200
        )

    # fig.add_scattergeo(
    #     locations=states['Code'],
    #     locationmode='USA-states',
    #     text=states['2024'],
    #     hoverinfo='skip',
    #     mode='text',
    #     showlegend=False
    #     )

    fig.update_layout(font=dict(
        size=10, 
        color="black"
        )),


    fig.update_traces(hovertemplate='<b>State: %{state}</b><br>Policy Count: %{2024}')

    fig.update_layout(
        title=dict(text="Active Policies by State", 
               #font=dict(size=18)
               ))
    return fig

def graph_binder_quote_differences():
    data = {'Comparison': ['Over', 'Equal to', 'Under'],
        'Binder': [1003, 22, 349],
        'Quote': [790, 15, 569]
       }

    df = pd.DataFrame(data)

    fig = make_subplots(rows=1, cols=2, 
                    specs=[[{"type": "pie"}, 
                            {"type": "pie"}]], 
                    subplot_titles = ("Policy vs Binder Amount", "Policy vs Quote Amount"
                                     ))

    fig.add_trace(go.Pie(values = df['Binder'],
                            labels = df['Comparison'],
                            domain = dict(x=[0, 0.5]),
                            name = "x",
                            marker ={'colors':['#056374', '#dc3828', '#738738']}
                            ),
                            row = 1, col = 1)

    fig.add_trace(go.Pie(values = df['Quote'],
                            labels = df['Comparison'],
                            domain = dict(x=[0.5, 1]),
                            name = "x",
                            marker ={'colors':['#056374', '#dc3828', '#738738']}
                            ),
                            row = 1, col = 2)

    fig.update_traces(
        hovertemplate='Count of Policies <b>%{label}</b> Quote Amount: %{value}'
    )

    fig.update_layout(title = 'Binder/Quote Differences', 
                    #title_x=.5, 
                    height=400
                    )

    return fig

def graph_lapse_rate():
    data = {'Insurance Type': ['Auto', 'Commercial', 'Life', 'Home'],
        'Percentage': [.67, .42, .31, .25],
        'Format': ['67%','42%', '31%', '25%'],
       }
    df = pd.DataFrame(data) 

    fig = px.bar(df, 
             x= "Insurance Type",
             y= "Percentage",
             text = 'Format',
             color_discrete_sequence = ['#056374'],
             title = "Lapse Rates<br><sup>*Average Lapse Rate Across All Policies Indicated by Dotted Line</sup>")
            
    fig.update_layout(  yaxis=dict(tickformat=".0%"), yaxis_title='% of Policies Not Renewed', height=400)

    fig.update_traces(
    hovertemplate='<b>Insurance Type: %{x}</b><br>Lapse Rate: %{text}'
    )
    fig.add_hline(y=.4125, line_width=2, line_dash='dash', line_color='white')

    return fig

def graph_conversion_funnel():
    data = dict(
    number=[ 3392, 2056, 1511, 1044],
    stage=["Leads Generated","Quotes Provided", "Policies Generated", "Policies Approved"])

# fig = px.funnel(data, x='number', y='stage', color = 'stage', 
# color_discrete_sequence =  ["#f7862b", '#738738','#dc3828',"#056374"], labels={'stage':'Funnel Step'})

    fig = go.Figure(go.Funnel(
    y = data['stage'],
    x = data['number'],
    text = data['stage'],
    textposition = "inside",
    #textinfo = "value+percent initial",
    #opacity = 0.65, 
    marker = {"color": ["#056374", '#dc3828', '#738738', "#f7862b"],
    #"line": {"width": [4, 2, 2, 3, 1, 1], "color": ["wheat", "wheat", "blue", "wheat", "wheat"]}
             },
    connector = {"line": {"color": "gray", "width": 3}})
    )

    fig.update_traces(
        hovertemplate='<b>Step: %{y}</b><br>Count: %{x}'
    )

    fig.update_layout(title = 'Conversion Funnel',  yaxis=dict(tickformat=".0%"), height=400)

    fig.update_yaxes(visible=False)

    return fig


st.write(graph_policy_breakdown_by_insurance_type())
# st.write(graph_policy_breakdown_by_state())
st.write(graph_monthly_trends())
st.write(graph_binder_quote_differences())
st.write(graph_lapse_rate())
st.write(graph_conversion_funnel())