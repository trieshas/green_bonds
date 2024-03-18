# Import Libraries
import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="Green Economy Dashboard",
    page_icon="🌿"
)

# Sidebar
with st.sidebar:
    st.title("📌 About")
    with st.expander("**📚 About This Dashboard**"):
        st.write("This dashboard presents the visualization of green bonds, environmental protection expenditures, and gross domestic product data to show the trend of green financing from countries around the world. Green financing, through green bonds, could be seen as one of the variables involved in transforming the world's fossil-fuel-based economy to a more sustainable and inclusive **green economy**.")
    with st.expander("**🔎 How To Use**"):
        st.write("In this dashboard, you can:")
        st.markdown("""
        * expand or hide text
        * observe the trend of green bonds issuance
        * view green bond issuers by year
        * see type of issuer by percentage or value
        * check out each countries' issued green bonds based on year and region
        * take a look at each country's environmental protection expenditure percentage and concern
        * multiselect some countries' annual gross domestic product
        """)
    with st.expander("**✨ About This Project**"):
        st.write("""This is a capstone project of TETRIS #Batch4 program.""")    
    with st.expander("**🌼 Author**"):
        st.write("**Triesha Syifahati**")
        st.write("[Click to connect!](https://www.linkedin.com/in/triesha-syifahati/)")
           
# Dashboard Title and Green Economy
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

# GREEN BONDS
st.header("💸 Green Bonds Overview")

# Dataset for Type of Issuer
issuer = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQ3FXcBVHwZ7e4ynMx8ptDEmR2UoiAcjxiJIf4lj-NJk1GdAXzvMt6vENKNW9hRnUZ34cKtcyoedA2C/pub?gid=193532952&single=true&output=csv'
df_issuer = pd.read_csv(issuer)

# Dataset for Green Bonds Issuance per Country
bond = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vS9E4_uHhawLaAkcSPxbilVAbxYjmZ8W0-5hP5lmuaMimayMH9QMej2CQbTL46tv0Cy1mneKkS00Cw_/pub?gid=2046901806&single=true&output=csv'
df_bond = pd.read_csv(bond)

# Create column and show metrics
country, issuer, total = st.columns(3)

with country:
    countries = df_bond['Country'].nunique()

    st.metric("✅ Country", value=countries, delta=None)

with issuer:
    issuers = df_issuer['Type_of_Issuer'].nunique()

    st.metric("📜 Type of Issuer", value=issuers, delta=None)

with total:
    # Calculate the sum of values for global green bonds issuance in 2022
    sum_2022 = df_issuer['2022'].sum()

    # Calculate the sum of values for global green bonds issuance in 2021
    sum_2021 = df_issuer['2021'].sum()

    sum_diff = 100.0 * (sum_2022 - sum_2021) / sum_2021

    st.metric("💡 Total in 2022", value=f'${sum_2022:.2f} B', delta=f'{sum_diff:.2f}%')

# About Green Bonds
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

# Melt to long format
df_melted = df_issuer.melt(id_vars='Type_of_Issuer', var_name='Year', value_name='Value')

# Group by Year and calculate the sum
df_sum = df_melted.groupby('Year')['Value'].sum().reset_index()

# Define a selection
selection = alt.selection_point(encodings=['x'])

# Calculate percentage difference
df_sum['Percentage Difference'] = df_sum['Value'].pct_change() * 100

# Create the chart
chart_sum = alt.Chart(df_sum).mark_bar(color='#2B6224').encode(
    x=alt.X('Year:O', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('Value:Q', title='Billion US Dollars'),
    tooltip=['Year', 'Value', 'Percentage Difference'],
    opacity=alt.condition(selection, alt.value(1), alt.value(0.5)),
).add_params(
    selection
).properties(
    width=600,
    height=400,
    title='Sum of Green Bonds Issuance by Year'
)

# Display Altair chart
st.altair_chart(chart_sum, use_container_width=True)

# Analysis
with st.expander('**💚 Analysis**'):
    st.markdown("""
            * The overall trend of green bonds seems to head towards an increase,
            as shown by the annual green bond issuance bar chart above.
            * The period with the least increase is from 2019 to 2020, which is around the COVID-19 outbreak period.
            * According to latest available data, we can observe that current's maximum participation
            seems to peak at year 2021.
            * The green bonds issued at 2021 is more than two times of green bonds issued at 2020 with around 115% of increase.
            * Although the cause behind this spike should be investigated further,
            it is safe to assume that this phenomenon happened because many countries are opting to finance sustainable projects after the COVID-19 outbreak
            * There seems to be a decline in the next year (2022), probably because of the Russian invasion of Ukraine that took place in February, affecting the world's overall economy.""")

# TYPE OF ISSUER
st.subheader("📑 Type of Issuer")

with st.expander("**📕 About Issuer**"):
    st.write("""
        ### 💷 Issuer
        In the context of bonds, an issuer refers to the entity that issues the bond and is responsible
        for making payments to bondholders. The issuer can be a corporation, government entity 
        (such as a national government or local municipality), or other organizations that seek to raise capital by issuing bonds.
       """)
    st.write("Type of green bond issuer:")
    st.markdown("""
    * Banks
    * International Organizations
    * Local and State Government
    * Nonfinancial Corporations
    * Other financial corporations
    * Sovereign
    * State owned entities
    """)

# Slider for year selection
selected_year = st.select_slider('Select Year', ['2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022'])

# Define color palette
color_palette = ["#E3F3E1", "#BDE2B9", "#7CC674", "#4CB140", "#38812F", "#2B6224", "#23511E"]
new_color_palette = ["#193A16", "#23511E", "#367D2F", "#59BD4F", "#8EC04C", "#B7CF3D", "#CBE626"]

# Sort the data by the selected year in descending order
sorted_df_issuer = df_issuer.sort_values(selected_year, ascending=False)

# Calculate the total sum for the selected year
total_sum = sorted_df_issuer[selected_year].sum()

# Calculate the percentage of each category
sorted_df_issuer['Percentage'] = sorted_df_issuer[selected_year] / total_sum * 100

# Create a selection
selection = alt.selection_point(fields=['Type_of_Issuer'])

# Create pie chart for Tab 1
pie_chart = alt.Chart(sorted_df_issuer).mark_arc().encode(
    alt.Color('Type_of_Issuer:N', 
              legend=alt.Legend(title='Type of Issuer'), 
              scale=alt.Scale(scheme='viridis')
              ).sort(field='Percentage', op='max', order='descending'),
    tooltip=['Type_of_Issuer', 'Percentage'],
    theta='Percentage:Q',
    order='Percentage:Q',
    opacity=alt.condition(selection, alt.value(1), alt.value(0.5))
).add_params(
    selection
).properties(
    width=400,
    height=400,
    title=f'Pie Chart for {selected_year}'
)

# Adjust the legend
pie_chart = pie_chart.configure_legend(labelLimit=0)  # Set labelLimit to 0 to show full category names

# Create Tab
tab1, tab2 = st.tabs(["🥧 Percentage Comparison", "💲 Value Comparison"])

# Tab 1
with tab1:
    st.altair_chart(pie_chart, use_container_width=True)

# Filter the DataFrame by selected year
df_filtered = df_melted[df_melted['Year'] == selected_year]

# Create dot chart for Tab 2
dot_chart = alt.Chart(df_filtered).mark_circle().encode(
    alt.X('Value:Q', axis=None),
    alt.Y('Type_of_Issuer:N', title='Type of Issuer', axis=alt.Axis(labelLimit=0)),
    size='Value:Q',
    color=alt.Color('Type_of_Issuer:N', scale=alt.Scale(scheme='viridis'), legend=None),
    tooltip=['Type_of_Issuer', 'Value']
).properties(
    width=600,
    height=400,
    title=f'Value Comparison for {selected_year} in Billion US Dollars'
).interactive()

# Tab 2
with tab2:
    st.altair_chart(dot_chart, use_container_width=True)

# Analysis
with st.expander('**💜 Analysis**'):
    st.markdown("""
    * Aligned with the issuance amount growth, the type of issuer involved in green bonds also grows over time, as seen by more diverse participation.
    * More than half of the green bonds in 2012 to 2013 are issued by International Organization such as World Bank.
    * In 2014, International Organization is also the biggest issuer despite contributing to lower percentage at around 34%. 
    * This is because there are more issuance from other issuers, such as Nonfinancial corporations that takes up around 27% of the issuance.
    * Around the next four years from 2015 to 2018, Nonfinancial corporations and Banks alternately became the top green bonds issuer.
    * From 2019 to 2022, only Nonfinancial corporations managed to preserve its position as the issuer with the most green bonds issuance globally.
    * In this period, we can also observe that Banks and Other financial corporations also stand out.
    """)

# BY REGION
st.subheader("🌏 Participation by Region")

# Year slider
year = st.slider('Select a year', min_value=2012, max_value=2022, value=2022, step=1)

# Data
region = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRc9gb_MCustazRQfq8Ue5AB-Ko8BKCpXJFCBVZXJUrziR--zeLgCuGR9ifvkwYCe8g1H4lfp3kA01c/pub?gid=731874032&single=true&output=csv'
df_region = pd.read_csv(region)
sy = str(year)

# For metrics values
africas = df_region.loc[df_region['Region']=='Africa',sy]
asias = df_region.loc[df_region['Region']=='Asia',sy]
europes = df_region.loc[df_region['Region']=='Europe',sy]
norths = df_region.loc[df_region['Region']=='North America',sy]
oceans = df_region.loc[df_region['Region']=='Oceania',sy]
souths = df_region.loc[df_region['Region']=='South America',sy]
alls = df_region[sy].sum()

# Column for metrics
texts, all, north, south = st.columns(4)
with texts:
    st.metric("⌛ Total in", value=year, delta=None)
with all:
    st.metric(label="🌈 All", value=alls, delta=None)  
with north:
    st.metric(label="🗽 North America", value=norths, delta=None)
with south:   
    st.metric("🏝️ South America", value=souths, delta=None)

# Column for metrics
africa, asia, europe, oceania = st.columns(4)
with africa:
    st.metric("🦁 Africa", value=africas, delta=None)
with asia:
    st.metric("🌸 Asia", value=asias, delta=None)
with europe:    
    st.metric("🏰 Europe", value=europes, delta=None)
with oceania:    
    st.metric("🐨 Oceania", value=oceans, delta=None)

# Color palette
color_palette_2 = ['#FFABAB', '#a75cf7','#ff5192','#FF6F2F','#ffc927','#ffff36']

# Function to create horizontal bar chart
def create_bar_chart(year, continent):
    melted_df = df_bond.melt(id_vars=['Country', 'Region'], var_name='Year', value_name='Value')
    filtered_df = melted_df[melted_df['Year'] == str(year)]
    filtered_df = filtered_df.dropna(subset=['Region'])  # Exclude rows with NULL in Continent column
    filtered_df = filtered_df[(filtered_df['Value'].notnull()) & (filtered_df['Value'] != 0)]

    if continent != 'All':
        filtered_df = filtered_df[filtered_df['Region'] == continent]

    chart = alt.Chart(filtered_df).mark_bar().encode(
        y=alt.Y('Country:N', title='Country', sort='-x', axis=alt.Axis(labelLimit=0)),
        x=alt.X('Value:Q', title='Billion US Dollars'),
        color=alt.Color('Region:N', scale=alt.Scale(range=color_palette_2)),
        tooltip=['Country', 'Value', 'Region']
    ).properties(
        title=f'Green Bonds Issuance by Country in {year}'
    )

    return chart

# Continent dropdown
filtered_df = df_bond.dropna(subset=['Region'])
continents = filtered_df['Region'].unique().tolist()
continents.insert(0, 'All')  # Add an option to select all continents
selected_continent = st.selectbox('Select a region', continents)

# Display the horizontal bar chart
st.altair_chart(create_bar_chart(year, selected_continent), use_container_width=True)

# Annual analysis
with st.expander('**🧡 Analysis**'):
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11 = st.tabs(['2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022'])
    with tab1:
        st.markdown("""
        * In 2012, there are only 4 countries participating in issuing green bonds.
        * The cumulative for this year is less than $1 Billion, because most of the green bonds issuance were from internationa organizations.
        * There are only 3 regions involved, with France dominating 62.7% of the total.
        """)

    with tab2:
        st.markdown("""
        * France is still the country with most issuance, followed by Norway that contributes to 19,1% of the total.
        * This year is the first time that Asian countries (Hong Kong & Korea) take part in the green bonds market.
        * From the total of 9 countries, most of them are from Europe.
        """)

    with tab3:
        st.markdown("""
        * All regions participate for the first time.
        * From 18 countries that are issuing the green bonds, half of them are European countries.
        * France managed to almost triple their green bonds issuance from the previous year.
        * Total green bonds issuance from countries reached its first double digit number, with almost 385% raise from 2013.
        """)

    with tab4:
        st.markdown("""
        * France is still the country with most green bonds issuance, contributing to 21.5% of the total.
        * The United States comes second, with only $400 millions difference with France.
        * This year's issuance is almost 1.5 times of 2014's issuance.
        """)

    with tab5:
        st.markdown("""
        * China (Mainland) significantly multiplying their green bonds issuance in 2016, resulting them to placed first.
        * A total of $29.2 billions are issued from a single country for the first time.
        * This happened because the Shanghai Pudong Development Bank was issuing their first green bonds this year. 
        """)

    with tab6:
        st.markdown("""
        * Both China and France issued more than $20 billions each.
        * China and France made up almost 1/3 of the green bonds issuance this year.
        * Netherlands issued more than $10 billions green bonds this year.
        """)

    with tab7:
        st.markdown("""
        * Not many changes since the last 2 year, because China still occupies the first spot.
        * Countries that managed to issued more than $10 billions of green bonds are China, France, Belgium, and Netherlands.
        * Indonesia entering the green bonds market in the 16th place, issuing around $2.5 billions.
        """)

    with tab8:
        st.markdown("""
        * Indonesia's green bonds issuance has decreased around $1 billions from previous year.
        * France, Netherlands, United States, and Germany issued more than $20 billions of green bonds.
        * Issuance from China is inching closer to $40 billions. 
        """)

    with tab9:
        st.markdown("""
        * Germany's green bonds issuance peaked at $43.6 billions.
        * Germany became an important player in the green bonds market after pioneering the first green federal security with its uniqueness as 'twin bonds'.
        * Indonesia increased its green bonds issuance around 20% from the previous year.
        """)

    with tab10:
        st.markdown("""
        * The number of countries issuing green bonds in 2021 is the highest so far, totaling up to 67 countries.
        * Germany increased their issuance to $74.4 billions.
        * China also significantly increased their presence in the green bonds market, issuing $71.4 billions.
        * Indonesia also issued more green bonds, totaling more than $2 billions.
        """)

    with tab11:
        st.markdown("""
        * China placed first with a total of $99.4 billions green bonds issuance.
        * Germany switched places with China, placing second with $83.8 billions of total issuance.
        * Indonesia managed to issue more than $5 billions green bonds.
        """)

# USE OF PROCEEDS

# Header and desc
st.header('📤 Cumulative Green Bond Issuances by Use of Proceeds')
with st.expander('**📂 About Cumulative Green Bond Issuances by Use of Proceeds**'):
    st.write("""
    ### 🚋 Cumulative Green Bond Issuances by Use of Proceeds
    Cumulative Green Bond Issuances by Use of Proceeds refers to the total amount of money raised through the issuance of green bonds, categorized based on the intended use of the funds.
    It provides an overview of the total funding raised through green bonds, broken down by the types of projects or activities they finance.
    This breakdown helps investors, policymakers, and other stakeholders understand how capital is being deployed to support various environmental objectives and priorities.
    In this dashboard, the data being used is the latest available data from the IMF, showing cumulative green bond issuances by use of proceeds in 2022 (Billion US Dollars). 
""")
    
# Data
use = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSLqvhg_bECvhbg9yLA7NoGX9VLOZNTMQcguN4jUtN3NHiCyI3weK2MQVLewEE-ghKeBJNDb8mvuI99/pub?gid=187166788&single=true&output=csv'
df_use = pd.read_csv(use)

# Values for metrics
climate = df_use[df_use['Category']=='Climate Change Mitigation & Adaptation'].shape[0]
energy = df_use[df_use['Category']=='Sustainable Energy & Transportation'].shape[0]
env = df_use[df_use['Category']=='Environmental & Conservation Projects'].shape[0]
fin = df_use[df_use['Category']=='Financial & Economic Development'].shape[0]
inf = df_use[df_use['Category']=='Infrastructure Development'].shape[0]
soc = df_use[df_use['Category']=='Social & Community Development'].shape[0]

# Columns for metrics
climate_count, inf_count, energy_count = st.columns(3)
with climate_count:
    st.metric('🌱 Climate Change', value = f'{climate} projects', delta = None)
with energy_count:
    st.metric('⚡️ Sustainable Energy', value = f'{energy} projects', delta = None)
with inf_count:
    st.metric('🏙️ Infrastructure Development', value = f'{inf} projects', delta = None)

# Columns for metrics
env_count, soc_count, fin_count = st.columns(3)
with fin_count:
    st.metric('💼 Financial & Economic', value = f'{fin} projects', delta = None)
with soc_count:
    st.metric('👫 Social & Community', value = f'{soc} projects', delta = None)
with env_count:
    st.metric('🌺 Environment & Conservation', value = f'{env} projects', delta = None)

df_cat = df_use
sum_use = df_use['Value'].sum() # Sum
usage_cat = df_use.groupby('Category')['Value'].sum().reset_index() # Group by
df_cat['Usage'] = usage_cat['Value'] # Rename
df_cat['Category'] = usage_cat['Category'] # Rename
df_cat['Percentage'] = df_cat['Usage'] / sum_use * 100 # Calculate percentage
df_cat = df_cat[df_cat['Category'].notnull()] # NOT NULL

# Selection
selection = alt.selection_point(fields=['Category'])

# Color palette
new_color_palette_6 = ["#23511E", "#367D2F", "#59BD4F", "#8EC04C", "#B7CF3D", "#CBE626"]

# Create pie chart
pie_use = alt.Chart(df_cat).mark_arc().encode(
    alt.Color('Category:N',
              legend=alt.Legend(title='Use of Green Bond Category'),
              scale=alt.Scale(range=new_color_palette_6)
              ).sort(field='Percentage', op='max', order='descending'),
    tooltip=['Category', 'Usage', 'Percentage'],
    theta='Percentage:Q',
    order='Percentage:Q',
    opacity=alt.condition(selection, alt.value(1), alt.value(0.5))
).add_params(
    selection
).properties(
    title='Use of Green Bond by Category in 2022'
)

# Configure legend
pie_use = pie_use.configure_legend(labelLimit=0)

# Show chart
st.altair_chart(pie_use, use_container_width=True)

# Analysis
with st.expander('**💛 Analysis**'):
    st.markdown("""
        * The cumulative green bond issuances by use of proceeds is categorized into 6 different categories.
        * Based on usage, the total amount of money raised through the issuance of green bonds in 2022 are mostly used to finance projects that falls into the Sustainable Energy & Transportation category.
        * More than half of the cumulative green bonds issuance, at around 63% are intended to fund Sustainable Energy & Transportation projects
        * At least 21% of the cumulative green bonds issuance are allocated to fund Climate Change Mitigation & Adaptation.
        * The rest four other categories are funded by 1-5% cumulative green bonds issuance, with the least funded being projects in the Social & Community Development category.
    """)

# Sizes
st.subheader('💐 Size of The Projects')

# Values for metrics
totals = df_use['Amount'].count()
hundreds = df_use[df_use['Amount']=='More than 100 Billions'].shape[0]
tens = df_use[df_use['Amount']=='Ten to 100 Billions'].shape[0]
single = df_use[df_use['Amount']=='One to 10 Billions'].shape[0]
less = df_use[df_use['Amount']=='Less Than 1 Billions'].shape[0]
mils = df_use[df_use['Amount']=='Less Than 100 Millions'].shape[0]

# Columns for metrics
totals_count, hundreds_count, tens_count, single_count, less_count, mils_count = st.columns(6)
with totals_count:
    st.metric(label='🌴 Total', value = totals, delta = None)
with hundreds_count:
    st.metric('🍁 &gt; $100 B', value = hundreds, delta = None)
with tens_count:
    st.metric('🍂 &gt; $10 B', value = tens, delta = None)
with single_count:
    st.metric('🌹 &gt; $1 B', value = single, delta = None)
with less_count:
    st.metric('🌷 &lt; $1 B', value = less, delta = None)
with mils_count:
    st.metric('🌾 &lt; $100 M', value = mils, delta = None)

# Data
df_pro = pd.read_csv(use)

# Selection
selection = alt.selection_point(encodings=['x'])

# Details and bar charts
with st.expander('**💟 Details**'):
    tab1, tab2, tab3 = st.tabs(['Sustainable Energy & Transportation','Climate Change Mitigation & Adaptation','Infrastructure Development'])
    with tab1:
        df_su = df_pro[df_pro['Category'] == 'Sustainable Energy & Transportation']
        total, max_column, min_column = st.columns(3)
        with total:
            total_b = df_su['Value'].sum()
            st.metric('Total', value = f'${total_b:.2f} B', delta = None)
        with max_column:
            maxcl = df_su['Value'].max()
            st.metric('Maximum', value = f'${maxcl:.2f} B', delta = None)
        with min_column:
            mincl = df_su['Value'].min()
            st.metric('Minimum', value = f'${mincl:.2f} B', delta = None)

        bar_chart = alt.Chart(df_su).mark_bar(color='#23511E').encode(
            y=alt.Y('Use_of_Proceed:N', sort='-x', title=None, axis=alt.Axis(labelLimit=0)),
            x=alt.X('Value:Q', title='Value'),
            opacity=alt.condition(selection, alt.value(1), alt.value(0.5)),
        ).add_params(
            selection
        )
        # Display the chart
        st.altair_chart(bar_chart, use_container_width = True)
    with tab2:
        df_cl = df_pro[df_pro['Category'] == 'Climate Change Mitigation & Adaptation']
        total, max_column, min_column = st.columns(3)
        with total:
            total_b = df_cl['Value'].sum()
            st.metric('Total', value = f'${total_b:.2f} B', delta = None)
        with max_column:
            maxcl = df_cl['Value'].max()
            st.metric('Maximum', value = f'${maxcl:.2f} B', delta = None)
        with min_column:
            mincl = df_cl['Value'].min()
            st.metric('Minimum', value = f'${mincl:.2f} B', delta = None)

        bar_chart = alt.Chart(df_cl).mark_bar(color='#367D2F').encode(
            y=alt.Y('Use_of_Proceed:N', sort='-x', title=None, axis=alt.Axis(labelLimit=0)),
            x=alt.X('Value:Q', title='Value'),
            opacity=alt.condition(selection, alt.value(1), alt.value(0.5)),
            ).add_params(
                selection
            )
        # Display the chart
        st.altair_chart(bar_chart, use_container_width = True)
    with tab3:
        df_in = df_pro[df_pro['Category'] == 'Infrastructure Development']
        total, max_column, min_column = st.columns(3)
        with total:
            total_b = df_in['Value'].sum()
            st.metric('Total', value = f'${total_b:.2f} B', delta = None)
        with max_column:
            maxcl = df_in['Value'].max()
            st.metric('Maximum', value = f'${maxcl:.2f} B', delta = None)
        with min_column:
            mincl = df_in['Value'].min()
            st.metric('Minimum', value = f'${mincl:.2f} B', delta = None)

        bar_chart = alt.Chart(df_in).mark_bar(color='#59BD4F').encode(
            y=alt.Y('Use_of_Proceed:N', sort='-x', title=None, axis=alt.Axis(labelLimit=0)),
            x=alt.X('Value:Q', title='Value'),
            opacity=alt.condition(selection, alt.value(1), alt.value(0.5)),
        ).add_params(
            selection
        )
        # Display the chart
        st.altair_chart(bar_chart, use_container_width = True)

    tab4, tab5, tab6 = st.tabs(['Environmental & Conservation Projects','Financial & Economic Development','Social & Community Development'])
    with tab4:
        df_en = df_pro[df_pro['Category'] == 'Environmental & Conservation Projects']
        total, max_column, min_column = st.columns(3)
        with total:
            total_b = df_en['Value'].sum()
            st.metric('Total', value = f'${total_b:.2f} B', delta = None)
        with max_column:
            maxcl = df_en['Value'].max()
            st.metric('Maximum', value = f'${maxcl:.2f} B', delta = None)
        with min_column:
            mincl = df_en['Value'].min()
            st.metric('Minimum', value = f'${mincl:.4f} B', delta = None)

        bar_chart = alt.Chart(df_en).mark_bar(color='#8EC04C').encode(
            y=alt.Y('Use_of_Proceed:N', sort='-x', title=None, axis=alt.Axis(labelLimit=0)),
            x=alt.X('Value:Q', title='Value'),
            opacity=alt.condition(selection, alt.value(1), alt.value(0.5)),
        ).add_params(
            selection
        )
        # Display the chart
        st.altair_chart(bar_chart, use_container_width = True)
    with tab5:
        df_fi = df_pro[df_pro['Category'] == 'Financial & Economic Development']
        total, max_column, min_column = st.columns(3)
        with total:
            total_b = df_fi['Value'].sum()
            st.metric('Total', value = f'${total_b:.2f} B', delta = None)
        with max_column:
            maxcl = df_fi['Value'].max()
            st.metric('Maximum', value = f'${maxcl:.2f} B', delta = None)
        with min_column:
            mincl = df_fi['Value'].min()
            st.metric('Minimum', value = f'${mincl:.4f} B', delta = None)

        bar_chart = alt.Chart(df_fi).mark_bar(color='#B7CF3D').encode(
            y=alt.Y('Use_of_Proceed:N', sort='-x', title=None, axis=alt.Axis(labelLimit=0)),
            x=alt.X('Value:Q', title='Value'),
            opacity=alt.condition(selection, alt.value(1), alt.value(0.5)),
        ).add_params(
            selection
        )
        # Display the chart
        st.altair_chart(bar_chart, use_container_width = True)
    with tab6:
        df_so = df_pro[df_pro['Category'] == 'Social & Community Development']
        total, max_column, min_column = st.columns(3)
        with total:
            total_b = df_so['Value'].sum()
            st.metric('Total', value = f'${total_b:.2f} B', delta = None)
        with max_column:
            maxcl = df_so['Value'].max()
            st.metric('Maximum', value = f'${maxcl:.2f} B', delta = None)
        with min_column:
            mincl = df_so['Value'].min()
            st.metric('Minimum', value = f'${mincl:.2f} B', delta = None)

        bar_chart = alt.Chart(df_so).mark_bar(color='#CBE626').encode(
            y=alt.Y('Use_of_Proceed:N', sort='-x', title=None, axis=alt.Axis(labelLimit=0)),
            x=alt.X('Value:Q', title='Value'),
            opacity=alt.condition(selection, alt.value(1), alt.value(0.5)),
        ).add_params(
            selection
        )
        # Display the chart
        st.altair_chart(bar_chart, use_container_width = True)

# ENVIRONMENTAL PROTECTION EXPENDITURES

# Data
data_link = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTdVY5KdcjHeaYhhpeVVeNnhqI7YVd-UlIs88oWtulNJsnzdtFdpZQuN32zW_4fxtLRbTUpS7qaf5JZ/pub?gid=402589920&single=true&output=csv"
dfe = pd.read_csv(data_link)

# Drop unnecessary columns
columns_to_drop = ['ObjectId', 'ISO2', 'ISO3', 'Source', 'CTS Code', 'CTS Name', 'CTS Full Descriptor']
dfe = dfe.drop(columns=columns_to_drop)

st.header('🌊 Environmental Protection Expenditures')
st.write('**In Percent of GDP**')
with st.expander('**💧 About Environmental Protection Expenditures**'):
    st.write("""
    ### 🧊 Environmental Protection Expenditures
    Environmental protection expenditure refers to the money spent by governments, businesses, or individuals on activities, projects, and initiatives aimed at preserving, conserving, and enhancing the environment. These expenditures are directed towards measures that mitigate environmental degradation, promote sustainability, and address environmental challenges such as pollution, habitat destruction, and climate change.
    \n Indicator by the IMF:
    """)
    st.markdown("""
    1. Expenditure on biodiversity & landscape protection
    2. Expenditure on environment protection
    3. Expenditure on environment protection R&D
    4. Expenditure on environment protection not elsewhere classified (n.e.c)
    5. Expenditure on pollution abatement
    6. Expenditure on waste management
    7. Expenditure on waste water management
    """)

selected_country = st.selectbox('Select Country', dfe['Country'].unique())

filtered_dfe = dfe[dfe['Country'] == selected_country]

# Melt dataframe to long format
melted_dfe = filtered_dfe.melt(id_vars=['Country', 'Indicator', 'Unit'], var_name='Year', value_name='Expenditure')
melted_dfe = melted_dfe[(melted_dfe['Expenditure'].notnull()) & (melted_dfe['Expenditure'] != 0)]

color_palette_21 = ['#0068C9','#7AC5FF','#a75cf7','#ff5192','#FF6F2F','#ffc927','#ffff36']

# Create chart
charte = alt.Chart(melted_dfe).mark_bar().encode(
    x=alt.X('Year:O', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('sum(Expenditure):Q', title = 'Percent of GDP'),
    color=alt.Color('Indicator:N', scale=alt.Scale(range=color_palette_21)),
    column='Country:N'
).properties(
    width=625,
    height=400
)

charte = charte.configure_legend(labelLimit=0, orient='bottom', columns=2)

# Display chart
st.altair_chart(charte)

with st.expander('**💙 Analysis**'):
    st.markdown("""
    * Currently there are 7 indicators regarding environmental protection expenditure by the IMF.
    * Each country might have different indicators or they might also only consider certain indicators in their budgeting.
    * There are countries like Indonesia that mostly allocate their budget to one of the indicators, which is 'expenditure on environmental protection'.
    * There are also countries that diversifies their budget according to all of the determined indicators, such as Austria.
    * Developed countries tend to be able to budget more for the enviromental protection expenditure, for example France which budgets 1-2% of GDP, Japan that budgets 1-2.8% of GDP, Netherlands that budgets 1-2.5% of GDP, etc.
    * This may be because developing countries have other urgent economic priorities, such as eradicating poverty, industrialization and economic diversification, infrastructure development, and more.            
    """)
