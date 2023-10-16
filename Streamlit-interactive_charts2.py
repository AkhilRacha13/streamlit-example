import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# Read data into a DataFrame
df = pd.read_csv("Python Exercise Data.csv")

# Parse dates in the DataFrame
df["Start"] = pd.to_datetime(df["Start Time"])
df["End"] = pd.to_datetime(df["End Time"])

# Create a Streamlit web app
st.title("Interactive Charts")

# Sidebar for filtering data
selected_machine = st.sidebar.selectbox("Select Machine ID", df["MachineID"].unique())
selected_state = st.sidebar.selectbox("Select State", df["State"].unique())

# Filter data based on selected machine
filtered_df = df[df["MachineID"] == selected_machine & df["State"] == selected_state]

# Create a timeline chart using Plotly Express
timeline_fig = px.timeline(
    filtered_df,
    x_start=filtered_df["Start"],
    x_end=filtered_df["End"],
    y="MachineID",
    color="State",
    title="Machine Activity Timeline",
    color_discrete_map={"Stopped": "orangered", "Idle": "blue", "Working": "green"}
)

# Customize the appearance
timeline_fig.update_yaxes(autorange="reversed")  # Reverse the order of MachineIDs
timeline_fig.update_yaxes(fixedrange=True)  # Lock/disable the vertical zoom
timeline_fig.update_xaxes(rangemode="tozero", showspikes=True, spikethickness=1, spikesnap="cursor", showline=True, showgrid=False)
timeline_fig.update_layout(xaxis=dict(rangeslider=dict(visible=True, thickness=0.05, bgcolor="lightgray")))

# Update the x-axis range to show the end timeline by default
timeline_fig.update_layout(
    xaxis=dict(range=[filtered_df["End"].max() - pd.Timedelta(hours=1), filtered_df["End"].max()])
)

# Create buttons to control the step size of the rangeslider
step_buttons = [
    dict(
        label="1 Hour",
        method="relayout",
        args=[{"xaxis.range": [filtered_df["End"].max() - pd.Timedelta(hours=1), filtered_df["End"].max()]}],
    ),
    dict(
        label="3 Hours",
        method="relayout",
        args=[{"xaxis.range": [filtered_df["Start"].min(), filtered_df["Start"].min() + pd.Timedelta(hours=3)]}],
    ),
    dict(
        label="6 Hours",
        method="relayout",
        args=[{"xaxis.range": [filtered_df["Start"].min(), filtered_df["Start"].min() + pd.Timedelta(hours=6)]}],
    ),
    dict(
        label="12 Hours",
        method="relayout",
        args=[{"xaxis.range": [filtered_df["Start"].min(), filtered_df["Start"].min() + pd.Timedelta(hours=12)]}],
    ),
]

# Add a dropdown for step selection under the legend
step_dropdown = [
    dict(
        buttons=step_buttons,
        direction="down",
        showactive=False,
        x=1.025,
        xanchor="left",
        y=0.1,  # Adjust the y position to place it under the legend
        yanchor="top",
    )
]

# Add the step dropdown to the layout
timeline_fig.update_layout(updatemenus=step_dropdown)

# Create a bar plot using Plotly Express
filtered_df['Duration'] = (filtered_df['End'] - filtered_df['Start']).dt.total_seconds() / 3600  # Duration in hours

bar_fig = px.bar(
    filtered_df,
    x='MachineID',
    y='Duration',
    color='State',
    title='Machine State Duration',
    color_discrete_map={'Stopped': 'orangered', 'Idle': 'blue', 'Working': 'green'}
)

# Customize the appearance
bar_fig.update_yaxes(title='Duration (Hours)')
bar_fig.update_xaxes(title='Machine ID')
bar_fig.update_layout(legend_title='State')

# Display the charts side by side
st.plotly_chart(timeline_fig, use_container_width=True)
st.plotly_chart(bar_fig, use_container_width=True)
