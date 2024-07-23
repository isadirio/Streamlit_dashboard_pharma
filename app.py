import streamlit as st 
import pandas as pd 
import datetime 
import plotly.express as px 
import plotly.graph_objects as go
import io

# reading the data from csv 
df =pd.read_csv('data/sales_augmented_final.csv')
df['datum'] = pd.to_datetime(df['datum'])

#################
# OVERALL LAYOUT
#################
st.set_page_config(layout='wide')
st.markdown('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

# title 
html_title = """
    <style>
    .title-test {
    font-weight:bold;
    padding:5px;
    border-radius:4px;
    font-size: 30px;
    }
    </style>
    <center><h1 class="title-test">Pharma sales - Interactive Dashboard</h1></center>"""
st.markdown(html_title, unsafe_allow_html=True)

#logo
st.sidebar.image('logo.png', use_column_width=False, width=200)  


##################
# FILTERS
##################
st.sidebar.title('Filters')
# for the Product
product = st.sidebar.selectbox('Product', df['product'].unique())
# for the date range
date_min = df['datum'].min().date()
date_max = df['datum'].max().date()
start_date, end_date = st.sidebar.slider(
    'Select Date Range',
    min_value=date_min,
    max_value=date_max,
    value=(date_min, date_max),
    format='YYYY-MM-DD'
)
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)


##################
# MAIN CONTENT 
##################
col1, col2 = st.columns([0.6, 0.4])


with col1: 
    ##################
    # KPIs
    ##################

    # filter the DataFrame
    filtered_df = df[(df['product'] == product) & (df['datum'].between(start_date, end_date))]
    
    # compute KPIs and then display them 
    total_units_sold = filtered_df['unit_sold'].sum()
    total_profit = (filtered_df['price'] * filtered_df['unit_sold']).sum()
    total_margin = (filtered_df['margin'] * filtered_df['unit_sold']).sum()

    col1_1, col1_2, col1_3 = st.columns(3)
    col1_1.metric(label="Total Units Sold", value=f"{total_units_sold:,.0f}")
    col1_2.metric(label="Total Profit", value=f"€{total_profit:,.0f}")
    col1_3.metric(label="Total Margin", value=f"€{total_margin:,.0f}")


    ##################
    # MAP of Italy
    ##################

    # group by city
    city_aggregated = filtered_df.groupby(['city', 'lat', 'lng']).agg({'unit_sold': 'sum'}).reset_index()
    city_aggregated['unit_sold'] = city_aggregated['unit_sold'].round(2)
    # create map with plotly
    fig = px.scatter_mapbox(
        city_aggregated,
        lat='lat',
        lon='lng',
        size='unit_sold',
        color='unit_sold',
        hover_name='city',
        hover_data={'lat': False, 'lng': False, 'unit_sold': True},
        size_max=20, #maximum size of the bubble
        zoom=5,
        center={"lat": 41.8719, "lon": 12.5674},  # center of Italy
        mapbox_style='carto-positron'
    )

    # title to the map
    fig.update_layout(
        title='Total Units sold per city in Italy',
        title_x=0, #0 far left, 0.5 center
        margin={"r":0,"t":40,"l":0,"b":0}
    )

    # display
    st.plotly_chart(fig, use_container_width=True)

with col2: 
    ##################
    # LIST OF ADDITIONAL VISUALIZATIONS 
    ##################

    st.subheader("Visualizations")
    with st.expander("Line chart - Price, Cost & Margin"):
        # line chart - price*unit_sold, cost*unit_sold e margin*unit_sold
        filtered_df['price_total'] = filtered_df['price'] * filtered_df['unit_sold']
        filtered_df['cost_total'] = filtered_df['cost'] * filtered_df['unit_sold']
        filtered_df['margin_total'] = filtered_df['margin'] * filtered_df['unit_sold']
    
        date_aggregated = filtered_df.groupby('datum').agg({'price_total': 'sum', 'cost_total': 'sum', 'margin_total': 'sum'}).reset_index()
        date_aggregated = date_aggregated.sort_values('datum')
        
        line_fig = go.Figure()
        line_fig.add_trace(go.Scatter(x=date_aggregated['datum'], y=date_aggregated['price_total'], mode='lines', name='Price * Units Sold'))
        line_fig.add_trace(go.Scatter(x=date_aggregated['datum'], y=date_aggregated['cost_total'], mode='lines', name='Cost * Units Sold'))
        line_fig.add_trace(go.Scatter(x=date_aggregated['datum'], y=date_aggregated['margin_total'], mode='lines', name='Margin * Units Sold', line=dict(color='yellow')))
        
        line_fig.update_layout(
            title=f"Price, Cost, and Margin Analysis for {product}",
            xaxis_title="Date",
            yaxis_title="Total Value",
            legend_title="Metric",
            margin={"r":0,"t":40,"l":0,"b":0}
        )
        
        st.plotly_chart(line_fig, use_container_width=True)

    with st.expander("Bar chart - Units sold by Weekday"):
        # bar chart - group by weekday
        weekday_aggregated = filtered_df.groupby('Weekday Name').agg({'unit_sold': 'sum'}).reset_index()
        weekday_aggregated = weekday_aggregated.sort_values('unit_sold', ascending=False)
        
        bar_fig = px.bar(
            weekday_aggregated,
            x='Weekday Name',
            y='unit_sold',
            title='Total Units Sold by Weekday',
            labels={'unit_sold': 'Total Units Sold', 'Weekday Name': 'Day of the Week'}
        )
        
        st.plotly_chart(bar_fig, use_container_width=True)

    with st.expander("Bar chart - Units sold by Month"):
        # bar chart - group by month 
        # first map the number to the months 
        month_map = {
            1: 'January', 2: 'February', 3: 'March', 4: 'April',
            5: 'May', 6: 'June', 7: 'July', 8: 'August',
            9: 'September', 10: 'October', 11: 'November', 12: 'December'
        }
        # group by month
        weekday_aggregated = filtered_df.groupby('Month').agg({'unit_sold': 'sum'}).reset_index()
        weekday_aggregated = weekday_aggregated.sort_values('unit_sold', ascending=False)
        
        # substitute month number to the name 
        weekday_aggregated['Month'] = weekday_aggregated['Month'].map(month_map)
        
        # sort the month
        month_order = [
            'January', 'February', 'March', 'April', 'May', 'June', 
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
        weekday_aggregated['Month'] = pd.Categorical(weekday_aggregated['Month'], categories=month_order, ordered=True)
        weekday_aggregated = weekday_aggregated.sort_values('Month')

        bar_fig = px.bar(
            weekday_aggregated,
            x='Month',
            y='unit_sold',
            title='Total Units Sold by Month',
            labels={'unit_sold': 'Total Units Sold', 'Month': 'Month'}
        )
        
        st.plotly_chart(bar_fig, use_container_width=True)

    with st.expander("Bar chart - Units sold by Region"):
        # bar chart - group by region
        region_aggregated = filtered_df.groupby('admin_name').agg({'unit_sold': 'sum'}).reset_index()
        region_aggregated = region_aggregated.sort_values('unit_sold', ascending=False)

        region_bar_fig = px.bar(
            region_aggregated,
            x='admin_name',
            y='unit_sold',
            title='Total Units Sold by Region',
            labels={'unit_sold': 'Total Units Sold', 'admin_name': 'Region'}
        )

        st.plotly_chart(region_bar_fig, use_container_width=True)
    
    ##################
    # DOWNLOAD BUTTON
    ##################
    st.subheader("Download Data")
    
    # Crea un buffer di memoria per il CSV
    buffer = io.StringIO()
    filtered_df.to_csv(buffer, index=False)
    buffer.seek(0) 

    st.download_button(
        label="Download Filtered Data as CSV",
        data=buffer.getvalue(),
        file_name="filtered_sales_data.csv",
        mime="text/csv"
    )








