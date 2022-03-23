import random
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

transport_min=-1
transport_max=1
accom_min=-1
accom_max=-1
foods_min = -1
foods_max=-1


st.set_page_config(page_title="Ola's Bridal Party - cost breakdown calculator",layout="wide")#, page_icon = st.image(image))


if 'activities' not in st.session_state:
    st.session_state['activities'] = [("Burlesque",100)]
    st.session_state['activities_objs'] = []

if "is_new_activity_open" not in st.session_state:
    st.session_state['is_new_activity_open']=False

random_activities=["Moon watching","Doing squats","Singing Livin' on a prayer","Trying to lick own elbow",
                   "Petting dogs","Collecting flowers","Watching cartoons","Digging tunnel to China","Cracking"
                                                                                                               "joints"]

#st.set_page_config(layout="wide")
st.title("Ola's Bridal party - Cost breakdown")
limit= st.text_input('Amount to be spent', '600')
st.subheader('Transportation')


option = st.selectbox(
     'How will we travel?',
     ('Train', 'Car'))

if(option == "Train"):
    cost_of_transport = st.text_input('Cost of the ticket (two ways)', '150')
    cost_of_transport_on_site= st.text_input('Cost of transportation on site', '20')
    transport_total = int(cost_of_transport) + int(cost_of_transport_on_site)
else:
    adv = st.checkbox('Advanced transport calculations')
    if not adv:
        cost_of_transport_fuel = st.text_input('Cost of fuel:', '250')
        cost_of_transport_on_site = st.text_input('Cost of transportation on site', '20')
        transport_total = int(cost_of_transport_fuel) + int(cost_of_transport_on_site)
    else:
        cost_of_transport_litres_per_100km = st.text_input('Litres of fuel 100km:', '10')
        cost_of_transport_cost_of_litre = st.text_input("Cost of single litre(pln):", '7')
        cost_of_transport_length = st.text_input('Length of whole route(km) - two ways:', '356')
        cost_of_transport_highway_fee = st.text_input('Cost of highway fees:', '20')
        cost_of_transport_on_site = st.text_input('Cost of transportation on site', '20')
        transport_total = float(cost_of_transport_highway_fee) + \
                          float(cost_of_transport_length) / 100 * float(cost_of_transport_cost_of_litre) *\
                          float(cost_of_transport_litres_per_100km) + float(cost_of_transport_on_site)

        cost_of_transport_deviation = st.text_input('Deviation/Reserve:', '10')
        cost_of_transport_deviation_calculation = transport_total/int(cost_of_transport_deviation)
        st.markdown("""
        <style>
        .big-font {
            font-size:20px !important;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown(f'<p class="big-font">Including {cost_of_transport_deviation}% deviation, total cost of transport is: ---> {transport_total + transport_total/float(cost_of_transport_deviation)}pln</p>', unsafe_allow_html=True)

st.subheader('Accomodation')
cost_of_accomodation = st.text_input('Cost of accomodation(total):', '220')
cost_of_accomodation_deviation = st.text_input('Deviation/Reserve:', '5')
st.markdown("""
<style>
.big-font {
    font-size:20px !important;
}
</style>
""", unsafe_allow_html=True)
try:
    accomodation_total_deviation_calculation =int(cost_of_accomodation) / float(cost_of_accomodation_deviation)
    accom_min=int(cost_of_accomodation)-accomodation_total_deviation_calculation
    accom_max=int(cost_of_accomodation)+accomodation_total_deviation_calculation
except Exception:
    accomodation_total_deviation_calculation=0
    accom_min,accom_max=int(cost_of_accomodation),int(cost_of_accomodation)
if accomodation_total_deviation_calculation==0:
    st.markdown(
        f'<p class="big-font">Total cost of transport is: ---> {cost_of_accomodation}pln</p>',
        unsafe_allow_html=True)
else:
    st.markdown(
        f'<p class="big-font">Including {cost_of_accomodation_deviation}% deviation, total cost of transport is between : ---> {int(cost_of_accomodation)-accomodation_total_deviation_calculation} and {int(cost_of_accomodation)+accomodation_total_deviation_calculation}pln</p>',
        unsafe_allow_html=True)


st.subheader('Food & Drinks')
cost_of_food = st.text_input('Cost of food', '160')
cost_of_drinks = st.text_input('Cost of drinks (alc)', '150')
total_cost_foods_drinks = int(cost_of_food) + int(cost_of_drinks)
cost_of_food_deviation = st.text_input('Deviation:', '0')

try:
    foods_total_deviation_calculation =int(total_cost_foods_drinks) / float(cost_of_food_deviation)
    foods_min=total_cost_foods_drinks-foods_total_deviation_calculation
    foods_max=total_cost_foods_drinks+foods_total_deviation_calculation
except Exception:
    foods_total_deviation_calculation=0
    foods_min,foods_max=total_cost_foods_drinks,total_cost_foods_drinks
if foods_total_deviation_calculation==0:
    st.markdown(
        f'<p class="big-font">Total cost of foods and drinks is: ---> {total_cost_foods_drinks}pln</p>',
        unsafe_allow_html=True)
else:
    st.markdown(
        f'<p class="big-font">Including {cost_of_food_deviation}% deviation, total cost of foods and drinks is between : ---> {int(total_cost_foods_drinks)-foods_total_deviation_calculation} and {int(total_cost_foods_drinks)+foods_total_deviation_calculation}pln</p>',
        unsafe_allow_html=True)



st.subheader("Activities")

def generate_knowledge_summary():
    pass
count=0
initial = True
def delete_from_activities(index):
    if initial:
        return
    del st. session_state['activities'][index]



for key,val in st.session_state['activities']:
    x = st.text_input(key,str(val))
    st.session_state['activities_objs'].append(x)
    st.session_state['activities'][count]=(key,x)
    #st.button(f"DELETE - {key.split(' ')[0]}",on_click=delete_from_activities)
    st.button(f"DELETE - {key.split(' ')[0]}",on_click=delete_from_activities,args=(count,))
    count+=1


def add_activity_panel():
    st.session_state['is_new_activity_open']=True

if (st.session_state['is_new_activity_open']):
    act_name = st.text_input(f"New activity name: ", random.choice(random_activities))

    def add_activity():
        st.session_state['activities'].append((act_name,0))
        #st.session_state['activities_objs'].append(act_name)
        st.session_state['is_new_activity_open'] = False


    st.button("Approve new activity",on_click=add_activity)
st.button("Add new activity",on_click=add_activity_panel)



activities_cost = sum([int(x[1]) for x in st.session_state['activities']])

total_cost = transport_total + activities_cost+int(cost_of_accomodation) + total_cost_foods_drinks

st.markdown("""
<style>
.big-font-res {
    font-size:60px !important;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

def generate_knowledge_summary():
    st.subheader("Summary:")
    knowledge_summary =  f"Way of transportation: {option} ->"

    try:
        cost_of_transport_deviation_calculation
        transport_min =transport_total - cost_of_transport_deviation_calculation
        transport_max = transport_total + cost_of_transport_deviation_calculation
        knowledge_summary += f"{round(transport_min,2)} <-> {round(transport_max,2)}<br>"


    except Exception:
        knowledge_summary += f"{transport_total}pln<br>"
        transport_min,transport_max = transport_total,transport_total

    knowledge_summary+=f"Accomodation -> "
    if accomodation_total_deviation_calculation !=0:
        accom_min = int(cost_of_accomodation)-accomodation_total_deviation_calculation
        accom_max=int(cost_of_accomodation)+accomodation_total_deviation_calculation
        knowledge_summary+=f"{accom_min} <-> {accom_max}<br>"
    else:
        knowledge_summary+=f"{cost_of_accomodation}<br>"

    knowledge_summary+=f"Foods & drinks -> "
    if(foods_total_deviation_calculation!=0):
        foods_min = total_cost_foods_drinks-foods_total_deviation_calculation
        foods_max = total_cost_foods_drinks+foods_total_deviation_calculation
        knowledge_summary+=f"{foods_min} <-> {foods_max}<br>"
    else:
        knowledge_summary+=f"{total_cost_foods_drinks}<br>"

    knowledge_summary+=f"Activities -> {activities_cost}pln:<br>"
    for activity in st.session_state['activities']:
        knowledge_summary += f"----{activity[0]} -> {activity[1]}pln<br>"

    #knowledge_summary+=f"Total for activities is: {activities_cost}"
    return knowledge_summary

#knowledge_summary=generate_knowledge_summary()
def show_summary():
    #st.write(generate_knowledge_summary())
    st.markdown(
    f'<p class="big-font">{generate_knowledge_summary()}</p>',
    unsafe_allow_html=True)


#st.button(f"Generate sumary!",on_click=show_summary)
show_summary()
true_total_cost = transport_total + int(cost_of_accomodation) + total_cost_foods_drinks+activities_cost
addition_for_bride = st.text_input("Percentage added for bride (cos she doesn't pay for herself)", "10")
true_total_cost *= 1 + float(addition_for_bride) / 100

min_costs=foods_min + accom_min + transport_min + int(activities_cost)

min_costs*= 1 + float(addition_for_bride) / 100

max_costs=foods_max + transport_max + accom_max + int(activities_cost)
max_costs*= 1 + float(addition_for_bride) / 100

if (min_costs!=max_costs):
    st.markdown(
        f'<p class="big-font-res">Total cost is between {round(min_costs,2)}pln and {round(max_costs,2)}</p>',
        unsafe_allow_html=True)
else:
    st.markdown(
    f'<p class="big-font-res">Total cost is {true_total_cost}</p>',
    unsafe_allow_html=True)


if (min_costs+max_costs)/2>int(limit):
    st.error(f"Including all deviations, total cost WILL be higher than planned - from {round(min_costs-int(limit),2)} up to {round(max_costs-int(limit),2)} over the limit")
elif max_costs>int(limit):
    st.error(
        f"Including all deviations, total cost might be higher than planned - up to {round(max_costs - int(limit),2)} over the limit")





#Histogram
#
#
# # Group data together
# hist_data = [float(transport_total),float(cost_of_accomodation),float(activities_cost), float(total_cost_foods_drinks)  ]
#
# group_labels = ['Transport','Accomodation', 'Activities','Foods & Drinks']
#
# # Create distplot with custom bin_size
# fig = ff.create_distplot(
#          hist_data, group_labels)#, bin_size=[.1, .25, .5, 1])
#
# # Plot!
# st.plotly_chart(fig, use_container_width=True)
#
#
#
#
#

#arr = np.random.normal(1, 1, size=100)
#
# import altair as alt
#
# source = pd.DataFrame({"category": ["Transportation","Accomodation",'Activities',"Foods & Drinks"], "value": [transport_total,
#                                                                                                               int(cost_of_accomodation),
#                                                                                                               activities_cost,
#                                                                                                               total_cost_foods_drinks]})
#
# base = alt.Chart(source).encode(
#     theta=alt.Theta("value:Q", stack=True), color=alt.Color("category:N", legend=None)
# )
#
# pie = base.mark_arc(outerRadius=120)
# text = base.mark_text(radius=140, size=20).encode(text="category:N")
#
# st.altair_chart(pie + text)
#
# st.markdown(
#     f'<p class="big-font-res"><br>Total cost of your trip is {total_cost}pln</p>',
#     unsafe_allow_html=True)
#
# initial=False
#
# #
# # st.write('You selected:', option)
# #
# # cost_of_transport = st.text_input('Cost of transportation', '150')
# # cost_of_accom = st.text_input('Cost of accomodation', '220')
# #
# #
# #
# #
# # hour_to_filter = st.slider('hour', 0, 23, 17)
# #
# #
# #
# #
# #
#
# DATE_COLUMN = 'date/time'
# DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
#          'streamlit-demo-data/uber-raw-data-sep14.csv.gz')
#
# def load_data(nrows):
#     data = pd.read_csv(DATA_URL, nrows=nrows)
#     lowercase = lambda x: str(x).lower()
#     data.rename(lowercase, axis='columns', inplace=True)
#     data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
#     return data
#
#
#
# data_load_state = st.text('Loading data...')
# # Load 10,000 rows of data floato the dataframe.
# data = load_data(10000)
# # Notify the reader that the data was successfully loaded.
# data_load_state.text('Loading data...done!')
#
#
# hist_values = np.histogram(
#     data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
#
# st.bar_chart(hist_values)
#
# hour_to_filter = st.slider('hour', 0, 23, 17)
#
#
#
#
