import plotly.express as px
import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

df = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vQeaKeMlun5oXjzClHc7QFeWEJlIS8r7JAp8dReouB3YDKdM3PHiRl-3VDwqlmLFuY9bKFAvNLl47mI/pub?gid=1600829116&single=true&output=csv')

with st.sidebar:
    st.title("📌 About")
    with st.expander("**📚 About This Dashboard**"):
        st.write("This dashboard presents the visualization of green bonds, environmental protection expenditures, and gross domestic product data to show the trend of green financing from countries around the world. Green financing, through green bonds, could be seen as one of the variables involved in transforming the world's fossil-fuel-based economy to a more sustainable and inclusive **green economy**.")
    with st.expander("**🔎 How To Use**"):
        st.write("In this dashboard, you can:")
        st.markdown("""
        * expand or hide text
        * view type of green bonds issuer by year
        * see type of issuer by percentage or value
        * check out each countries' issued green bonds based on year and continent
        * select each country's environmental protection expenditures percentage and concern
        * multiselect some countries' annual gross domestic product
        """)
    with st.expander("**✨ About This Project**"):
        st.write("""This is a capstone project of TETRIS #Batch4 program.""")    
    with st.expander("**🌼 Author**"):
        st.write("**Triesha Syifahati**")
        st.write("[Click to connect!](https://www.linkedin.com/in/triesha-syifahati/)")
    


st.title("🌿 Green Economy Dashboard")
with st.expander("**📃 About Green Economy**"):
    st.write("""
             ### 🌳 Green Economy
        
            The green economy refers to an economic system that aims to reduce environmental risks and ecological scarcities, while promoting sustainable development. It encompasses various sectors and industries that prioritize environmental sustainability, resource efficiency, and social inclusiveness. Key components of the green economy include renewable energy, sustainable agriculture, waste management, eco-friendly transportation, and green technologies.
            The transition to a green economy is essential for addressing pressing environmental challenges such as climate change, biodiversity loss, and pollution. By promoting sustainable practices and investments, the green economy offers opportunities for economic growth, job creation, and improved quality of life. It fosters innovation, resilience, and long-term prosperity, while mitigating the adverse impacts of unsustainable development on ecosystems and communities.
            Countries that don't participate in green economy might face several risks, such as 
             """)
    st.markdown("""
            * the inability to export goods that don't comply with green standards,
            * limited accessibility with the global finance market, and 
            * lost opportunities due to investors investing in other countries with low-carbon industry.
            """)


st.header("💸 Green Bonds Overview")

country, issuer, total = st.columns(3)

with country:
    countries = df['Country'].nunique()

    st.metric("✅ Country", value=countries, delta=None)

with issuer:
    issuers = df.loc[df['Type_of_Issuer']!='Not Applicable']

    st.metric("📜 Type of Issuer", value=len(issuers), delta=None)

with total:
    df_subset = df.iloc[:107].reset_index(drop=True)
    # Calculate the sum of values for each country in 2022
    sum_2022 = df_subset['2022'].sum()

    # Calculate the sum of values for each country in 2021
    sum_2021 = df_subset['2021'].sum()

    sum_diff = 100.0 * (sum_2022 - sum_2021) / sum_2021

    st.metric("💡 Total in 2022", value=sum_2022, delta=f'{sum_diff:.2f}%')

with st.expander("**💰 About Green Bonds**"):
    st.write("""
        ### 🍃 Green Bonds
        
        Green bonds are financial instruments specifically designed to raise capital for projects with environmental benefits.
        These bonds are typically issued by governments, municipalities, corporations, or financial institutions to fund projects such as 
        """)
    st.markdown("""
            * renewable energy infrastructure, 
            * energy efficiency improvements,  
            * climate adaptation initiatives, and 
            * conservation efforts. 
            """)
    st.write("""
    The proceeds from green bond issuances are earmarked for environmentally sustainable projects, providing investors with an opportunity to support climate action and environmental stewardship.
    \n
    Green bonds play a crucial role in financing the transition to a green economy by channeling capital towards environmentally sustainable projects. These bonds enable governments, businesses, and organizations to raise funds for renewable energy, clean transportation, sustainable infrastructure, and other green initiatives.
    \n By facilitating investments in low-carbon technologies and climate-resilient infrastructure, green bonds contribute to the growth of green industries, the reduction of greenhouse gas emissions, and the advancement of sustainable development goals.
    \n Additionally, green bonds promote transparency, accountability, and best practices in environmental finance, helping to build investor confidence and support the mainstreaming of sustainable investment principles.
    
    """)

# Extract the columns you want to keep (Country, and the columns to be melted)
columns_to_keep = ['Country', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022']
df_subset_col = df_subset[columns_to_keep]

# Melt the DataFrame to long format
df_melted = df_subset_col.melt(id_vars='Country', var_name='Year', value_name='Value')

# Group by Year and calculate the sum
df_sum = df_melted.groupby('Year')['Value'].sum().reset_index()

chart_sum = alt.Chart(df_sum).mark_bar(color='green').encode(
    x='Year:O',
    y='Value:Q'
).properties(
    width=600,
    height=400,
    title='Sum of Green Bonds Issuance by Year (Billion US Dollar)'
)

# Display Altair chart
st.altair_chart(chart_sum, use_container_width=True)

st.markdown("""
         * The overall trend of green bonds seems to head towards an incline,
         as shown by the annual green bonds issuance bar chart above.
         * According to latest available data, we can observe that current's maximum participation
         seems to peak at year 2021.
         * Although the cause behind this spike should be investigated further,
         it is safe to assume that this phenomenon happen because many countries are opting for financing sustainable projects after the COVID-19 hit.
         * There seems to be a decline in the next year (2022), presumably because of the Russian invasion of Ukraine that took place in February, affecting the world's overall economy.""")

df_categories = df.iloc[107:114]

st.subheader("📑 Type of Issuer")
# selected_year = st.selectbox('Select Year', ['2018', '2019', '2020'])
# Slider for year selection
selected_year = st.select_slider('Select Year', ['2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022'])

fig_pie = px.pie(df_categories, names='Type_of_Issuer', values=selected_year,
             title=f'Pie Chart for {selected_year}')

tab1, tab2 = st.tabs(["🟢 Percentage Comparison", "🟢 Value Comparison"])

with tab1:
    st.plotly_chart(fig_pie, use_container_width=True)

# Melt the DataFrame to long format
df_melted = df_categories.melt(id_vars='Type_of_Issuer', var_name='Year', value_name='Value')

# Filter the DataFrame by selected year
df_filtered = df_melted[df_melted['Year'] == selected_year]

# Create the pie chart using Altair
pie_chart = alt.Chart(df_filtered).mark_circle().encode(
    alt.X('Value:Q', axis=None),
    alt.Y('Type_of_Issuer:N', title='Type of Issuer'),
    size='Value:Q',
    color='Type_of_Issuer:N',
    tooltip=['Type_of_Issuer', 'Value']
).properties(
    width=600,
    height=400,
    title=f'Value Comparison for {selected_year}'
).interactive()

with tab2:
    # Display the pie chart
    st.altair_chart(pie_chart, use_container_width=True)

st.markdown("""
* Aligned with the values growth, the type of issuer involved in green bonds also grow over time, as seen by more diverse participation.
* In year 2022, besides other financial corporations, we could observe that local and state government issue more green bonds than other organizations.
""")

st.subheader("🌐 Participation by Continent")
africa, asia, europe, north, oceania, south = st.columns(6)

with africa:
    africas = df.loc[df['Region']=='Africa']

    st.metric("🌍 Africa", value=len(africas), delta=None)

with asia:
    asias = df.loc[df['Region']=='Asia']

    st.metric("🌏 Asia", value=len(asias), delta=None)

with europe:
    europes = df.loc[df['Region']=='Europe']

    st.metric("🌍 Europe", value=len(europes), delta=None)

with north:
    norths = df.loc[df['Region']=='North America']

    st.metric("🌎 North America", value=len(norths), delta=None)

with oceania:
    oceans = df.loc[df['Region']=='Oceania']

    st.metric("🌏 Oceania", value=len(oceans), delta=None)

with south:
    souths = df.loc[df['Region']=='South America']

    st.metric("🌎 South America", value=len(souths), delta=None)


# Function to create Altair horizontal bar chart
def create_bar_chart(year, continent):
    melted_df = df.melt(id_vars=['Country', 'Region'], var_name='Year', value_name='Value')
    filtered_df = melted_df[melted_df['Year'] == str(year)]
    filtered_df = filtered_df.dropna(subset=['Region'])  # Exclude rows with NULL in Continent column
    filtered_df = filtered_df[(filtered_df['Value'].notnull()) & (filtered_df['Value'] != 0)]

    if continent != 'All':
        filtered_df = filtered_df[filtered_df['Region'] == continent]

    chart = alt.Chart(filtered_df).mark_bar().encode(
        y=alt.Y('Country:N', title='Country', sort='-x'),
        x=alt.X('Value:Q', title='Value'),
        color='Region:N',
        tooltip=['Country', 'Value', 'Region']
    ).properties(
        title=f'Green Bonds Issuance by Country in {year} (Billion US Dollar)'
    )

    return chart

# st.subheader('Green Bond Issuances by Country')
# st.write("This dashboard visualizes green bond issuances by country grouped by continent using Altair.")

# Year slider
year = st.slider('Select a year', min_value=2012, max_value=2022, value=2022, step=1)

# Continent dropdown
filtered_df = df.dropna(subset=['Region'])
continents = filtered_df['Region'].unique().tolist()
continents.insert(0, 'All')  # Add an option to select all continents
selected_continent = st.selectbox('Select a continent', continents)

# Sorting method
#sort_by = st.checkbox('Ascending')

# Display the horizontal bar chart
st.subheader(f'📗 Green Bonds Issuance by Country in {year} (Billion US Dollar)' )
st.write("This horizontal bar chart shows green bond issuances by country grouped by continent.")
st.altair_chart(create_bar_chart(year, selected_continent), use_container_width=True)
st.markdown("""
* Countries from the Europe continent dominates the top 10 spot for green bonds issuance.
* Next after the European countries are Asian countries with 2 of the 3 countries located in South East Asia.
* China is the largest green bonds issuer among countries in Asia continent, the only country included in the top 5.
            """)

# ENVIRONMENTAL PROTECTION EXPENDITURES

data_link = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTdVY5KdcjHeaYhhpeVVeNnhqI7YVd-UlIs88oWtulNJsnzdtFdpZQuN32zW_4fxtLRbTUpS7qaf5JZ/pub?gid=402589920&single=true&output=csv"
dfe = pd.read_csv(data_link)

# Drop unnecessary columns
columns_to_drop = ['ObjectId', 'ISO2', 'ISO3', 'Source', 'CTS Code', 'CTS Name', 'CTS Full Descriptor']
dfe = dfe.drop(columns=columns_to_drop)

# Multi-select box for selecting countries
st.header('🌊 Environmental Protection Expenditures')
st.write('**In Percent of GDP**')
with st.expander('**💧 About Environmental Protection Expenditures**'):
    st.write("""
    **According to the International Monetary Fund (IMF):**
    \n Government expenditures on a specified set of activities including pollution abatement, protection of biodiversity landscape, waste and wastewater management, within the framework of the Classification of Functions of Government (COFOG).
    """)

selected_country = st.selectbox('Select Country', dfe['Country'].unique())

# Filter dataframe based on selected countries
filtered_dfe = dfe[dfe['Country'] == selected_country]

# Melt dataframe to long format for Altair
melted_dfe = filtered_dfe.melt(id_vars=['Country', 'Indicator', 'Unit'], var_name='Year', value_name='Expenditure')
melted_dfe = melted_dfe[(melted_dfe['Expenditure'].notnull()) & (melted_dfe['Expenditure'] != 0)]

# Create Altair chart
charte = alt.Chart(melted_dfe).mark_bar().encode(
    x='Year:O',
    y='sum(Expenditure):Q',
    color='Indicator:N',
    column='Country:N'
).properties(
    width=alt.Step(20),
    height=400
).configure_axisX(labelAngle=45)

# Display chart
st.altair_chart(charte, use_container_width=True)

# GROSS DOMESTIC PRODUCT
st.header('🗺 Gross Domestic Product')
st.write('**GDP (current US$)**')

with st.expander("**📈 About Gross Domestic Product (GDP)**"):
    st.write("""
        ### Gross Domestic Product (GDP)
        
        Gross Domestic Product (GDP) is a key indicator of a country's economic performance. It represents the total monetary value of all goods and services produced within a country's borders over a specific period, typically a year or a quarter. GDP is often used as a measure of the size and health of an economy.
        
       """)

df_gdp = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vTdVY5KdcjHeaYhhpeVVeNnhqI7YVd-UlIs88oWtulNJsnzdtFdpZQuN32zW_4fxtLRbTUpS7qaf5JZ/pub?gid=1068216608&single=true&output=csv')

# Multi-select box for selecting countries
selected_countries = st.multiselect('Select Countries', df_gdp['Country'], default=['Indonesia'])

# Filter dataframe based on selected countries
filtered_df_gdp = df_gdp[df_gdp['Country'].isin(selected_countries)]

# Melt dataframe to long format for Altair
melted_df_gdp = filtered_df_gdp.melt(id_vars='Country', var_name='Year', value_name='GDP')

# Create Altair chart
chart_gdp = alt.Chart(melted_df_gdp).mark_line().encode(
    x='Year:O',
    y='GDP:Q',
    color='Country:N'
).properties(
    width=600,
    height=400
).interactive()

# Display chart
st.altair_chart(chart_gdp, use_container_width=True)

# txt, cha = st.columns([1,9])
# with txt:
#     st.write('something')
# with cha:
#     st.altair_chart(charte, use_container_width=True)

# BATAS SUCI
# data = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTdVY5KdcjHeaYhhpeVVeNnhqI7YVd-UlIs88oWtulNJsnzdtFdpZQuN32zW_4fxtLRbTUpS7qaf5JZ/pub?gid=1155855377&single=true&output=csv"

# df = pd.read_csv(data)

# # Melt the DataFrame to long format for Altair
# df_melted = pd.melt(df, id_vars=['country_name'], value_vars=['amount_exp', 'gdp_min'], var_name='metric', value_name='value')

# # Stacked bar chart for amount_exp and gdp_min
# bar_chart = alt.Chart(df_melted).mark_bar().encode(
#     y=alt.Y('country_name:N', title='Country', sort='-x'),
#     x='value:Q',
#     color='metric:N',
#     tooltip=['country_name', 'metric', 'value']
# ).properties(
#     width=400,
#     height=300
# )

# # Circle chart for sumgb
# circle_chart = alt.Chart(df).mark_circle().encode(
#     y=alt.Y('country_name:N', sort = '-x'),
#     x='sumgb:Q',
#     size=alt.Size('sumgb:Q', title='sumgb'),
#     tooltip=['country_name', 'sumgb']
# ).properties(
#     width=400,
#     height=300
# )

# # Combine the two charts
# combined_chart = bar_chart + circle_chart

# # Display the combined chart
# st.altair_chart(bar_chart, use_container_width = True)
# st.altair_chart(combined_chart, use_container_width = True)


# countries = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT5XeSzDT6OHcdJkIp9wGlmCIfrTTBWviZfQS8A--hX2FxHFwM_klzCk94Bbox9z3RUoLfeP9Sh17gP/pub?gid=1596994185&single=true&output=csv'
# dfc = pd.read_csv(countries)

# # Melt the dataframe to long format for Altair
# dfc_melted = pd.melt(dfc, id_vars=['country_name', 'indicator', 'unit'], var_name='year', value_name='value')

# # Line Chart: Trend of each indicator over time for each country
# line_chartt = alt.Chart(dfc_melted).mark_line().encode(
#     x='year:O',
#     y='value:Q',
#     color='indicator:N',
#     strokeDash='country_name:N',
#     tooltip=['country_name', 'indicator', 'value']
# ).properties(
#     width=600,
#     height=400
# ).interactive()

# # Grouped Bar Chart: Comparison of different indicators for each country across years
# grouped_bar_chartt = alt.Chart(dfc_melted).mark_bar().encode(
#     x=alt.X('year:N', title='Year'),
#     y=alt.Y('value:Q', title='Value'),
#     color='indicator:N',
#     column='country_name:N',
#     tooltip=['country_name', 'indicator', 'value']
# ).properties(
#     width=100,
#     height=400
# ).interactive()

# # Stacked Bar Chart: Composition of each indicator for each country across years
# stacked_bar_chartt = alt.Chart(dfc_melted).mark_bar().encode(
#     x=alt.X('year:N', title='Year'),
#     y=alt.Y('value:Q', title='Value', stack='zero'),
#     color='indicator:N',
#     column='country_name:N',
#     tooltip=['country_name', 'indicator', 'value']
# ).properties(
#     width=100,
#     height=400
# ).interactive()

# line, group, bar = st.columns(3)
# # Display the charts
# with line:
#     st.altair_chart(line_chartt, use_container_width=True)

# with group:
#     st.altair_chart(grouped_bar_chartt, use_container_width=True)

# with bar:
#     st.altair_chart(stacked_bar_chartt, use_container_width=True)


