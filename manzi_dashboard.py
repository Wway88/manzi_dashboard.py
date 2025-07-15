import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
from datetime import datetime, timedelta
import random

# Set page config
st.set_page_config(
    page_title="Manzi Water - Executive Dashboard",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Manzi brand colors and styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #059669 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .kpi-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1e3a8a;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .kpi-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1e3a8a;
        margin: 0;
    }
    .kpi-label {
        font-size: 1rem;
        color: #6b7280;
        margin: 0;
    }
    .status-green {
        color: #059669;
        font-weight: bold;
    }
    .status-red {
        color: #dc2626;
        font-weight: bold;
    }
    .status-yellow {
        color: #d97706;
        font-weight: bold;
    }
    .metric-annotation {
        font-size: 0.8rem;
        color: #6b7280;
        font-style: italic;
    }
    .tab-content {
        padding: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Generate sample data
@st.cache_data
def generate_sample_data():
    # Date range for historical data
    dates = pd.date_range(start='2022-01-01', end='2024-12-31', freq='D')
    
    # KPI data
    kpi_data = []
    for date in dates:
        # Add seasonal and trend patterns
        day_of_year = date.timetuple().tm_yday
        year = date.year
        
        # Reservoir levels (seasonal pattern)
        reservoir_base = 75 + 20 * np.sin(2 * np.pi * day_of_year / 365)
        if year == 2024 and date.month in [4, 5, 6]:  # Q2 2024 load shedding
            reservoir_base -= 15
        reservoir_level = max(20, reservoir_base + np.random.normal(0, 5))
        
        # Leakage rate (improving trend)
        leakage_base = 25 - (year - 2022) * 2
        leakage_rate = max(10, leakage_base + np.random.normal(0, 2))
        
        # Pump uptime
        pump_base = 95 - (5 if year == 2024 and date.month in [4, 5, 6] else 0)
        pump_uptime = min(100, max(80, pump_base + np.random.normal(0, 3)))
        
        # Billing vs Collection
        billing_efficiency = min(100, max(70, 85 + np.random.normal(0, 5)))
        
        # Energy costs (affected by load shedding)
        energy_base = 2.5 + (year - 2022) * 0.3
        if year == 2024 and date.month in [4, 5, 6]:
            energy_base *= 1.4
        energy_cost = max(1, energy_base + np.random.normal(0, 0.2))
        
        # SANS 241 compliance
        compliance = min(100, max(85, 96 + np.random.normal(0, 2)))
        
        # CSAT
        csat_base = 78 - (3 if year == 2024 and date.month in [4, 5, 6] else 0)
        csat = min(100, max(60, csat_base + np.random.normal(0, 4)))
        
        kpi_data.append({
            'date': date,
            'reservoir_level': reservoir_level,
            'leakage_rate': leakage_rate,
            'pump_uptime': pump_uptime,
            'billing_efficiency': billing_efficiency,
            'energy_cost': energy_cost,
            'compliance': compliance,
            'csat': csat
        })
    
    return pd.DataFrame(kpi_data)

# Generate geographical data
@st.cache_data
def generate_geo_data():
    # South African cities coordinates (approximated)
    locations = [
        {'city': 'Johannesburg', 'lat': -26.2041, 'lon': 28.0473},
        {'city': 'Cape Town', 'lat': -33.9249, 'lon': 18.4241},
        {'city': 'Durban', 'lat': -29.8587, 'lon': 31.0218},
        {'city': 'Pretoria', 'lat': -25.7479, 'lon': 28.2293},
        {'city': 'Port Elizabeth', 'lat': -33.9608, 'lon': 25.6022},
        {'city': 'Bloemfontein', 'lat': -29.0852, 'lon': 26.1596},
        {'city': 'East London', 'lat': -33.0153, 'lon': 27.9116},
        {'city': 'Polokwane', 'lat': -23.9045, 'lon': 29.4689},
        {'city': 'Nelspruit', 'lat': -25.4653, 'lon': 30.9700},
        {'city': 'Kimberley', 'lat': -28.7282, 'lon': 24.7499}
    ]
    
    geo_data = []
    for loc in locations:
        # Generate random incidents around each city
        for _ in range(np.random.randint(5, 15)):
            incident_type = np.random.choice(['pipe_burst', 'pump_outage', 'refill_station'], 
                                           p=[0.4, 0.3, 0.3])
            
            # Add some random offset to coordinates
            lat_offset = np.random.uniform(-0.1, 0.1)
            lon_offset = np.random.uniform(-0.1, 0.1)
            
            severity = np.random.choice(['High', 'Medium', 'Low'], p=[0.2, 0.5, 0.3])
            
            geo_data.append({
                'lat': loc['lat'] + lat_offset,
                'lon': loc['lon'] + lon_offset,
                'city': loc['city'],
                'type': incident_type,
                'severity': severity,
                'timestamp': datetime.now() - timedelta(days=np.random.randint(0, 30))
            })
    
    return pd.DataFrame(geo_data)

# Load data
df_kpis = generate_sample_data()
df_geo = generate_geo_data()

# Header
st.markdown("""
<div class="main-header">
    <h1>🌊 Manzi Water - Executive Dashboard</h1>
    <p>Enterprise Water Management Platform | $8.8M USD System Value</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🎛️ Dashboard Controls")
st.sidebar.markdown("---")

# Date range selector
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(datetime(2024, 1, 1), datetime(2024, 12, 31)),
    min_value=datetime(2022, 1, 1),
    max_value=datetime(2024, 12, 31)
)

# Filter data based on date range
if len(date_range) == 2:
    mask = (df_kpis['date'] >= pd.Timestamp(date_range[0])) & (df_kpis['date'] <= pd.Timestamp(date_range[1]))
    df_filtered = df_kpis[mask]
else:
    df_filtered = df_kpis

# Current metrics for KPI cards
current_metrics = df_filtered.tail(1).iloc[0] if not df_filtered.empty else df_kpis.tail(1).iloc[0]

# Main tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Executive Overview", "🗺️ Geo Intelligence", "🤖 AI Analytics", "🌱 ESG Dashboard", "📱 Mobile Field Ops"])

# Tab 1: Executive Overview
with tab1:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    
    # KPI Cards Row 1
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <p class="kpi-value">{current_metrics['reservoir_level']:.1f}%</p>
            <p class="kpi-label">Reservoir Level</p>
            <p class="metric-annotation">Seasonal variation +5% vs Q1</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <p class="kpi-value">{current_metrics['leakage_rate']:.1f}%</p>
            <p class="kpi-label">System Leakage</p>
            <p class="metric-annotation">Target: <15% by 2025</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <p class="kpi-value">{current_metrics['pump_uptime']:.1f}%</p>
            <p class="kpi-label">Pump Uptime</p>
            <p class="metric-annotation">Load shedding impact Q2 2024</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <p class="kpi-value">{current_metrics['billing_efficiency']:.1f}%</p>
            <p class="kpi-label">Billing Efficiency</p>
            <p class="metric-annotation">Collection vs Billing</p>
        </div>
        """, unsafe_allow_html=True)
    
    # KPI Cards Row 2
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.markdown(f"""
        <div class="kpi-card">
            <p class="kpi-value">R{current_metrics['energy_cost']:.2f}</p>
            <p class="kpi-label">Energy Cost/m³</p>
            <p class="metric-annotation">Load shedding spike Q2 2024</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        st.markdown(f"""
        <div class="kpi-card">
            <p class="kpi-value">{current_metrics['compliance']:.1f}%</p>
            <p class="kpi-label">SANS 241 Compliance</p>
            <p class="metric-annotation">Water Quality Standards</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col7:
        st.markdown(f"""
        <div class="kpi-card">
            <p class="kpi-value">{current_metrics['csat']:.1f}</p>
            <p class="kpi-label">Customer Satisfaction</p>
            <p class="metric-annotation">NPS Score (1-100)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col8:
        st.markdown(f"""
        <div class="kpi-card">
            <p class="kpi-value">28°C</p>
            <p class="kpi-label">Climate Forecast</p>
            <p class="metric-annotation">7-day avg temperature</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts Section
    st.markdown("## 📈 Performance Trends")
    
    # Multi-metric time series
    col1, col2 = st.columns(2)
    
    with col1:
        fig_reservoir = px.line(df_filtered, x='date', y='reservoir_level', 
                               title='Reservoir Levels Over Time',
                               color_discrete_sequence=['#1e3a8a'])
        fig_reservoir.add_hline(y=50, line_dash="dash", line_color="red", 
                               annotation_text="Critical Level")
        fig_reservoir.update_layout(height=400)
        st.plotly_chart(fig_reservoir, use_container_width=True)
    
    with col2:
        fig_leakage = px.line(df_filtered, x='date', y='leakage_rate',
                             title='System Leakage Rate Reduction',
                             color_discrete_sequence=['#059669'])
        fig_leakage.add_hline(y=15, line_dash="dash", line_color="green", 
                             annotation_text="2025 Target")
        fig_leakage.update_layout(height=400)
        st.plotly_chart(fig_leakage, use_container_width=True)
    
    # Combined performance chart
    fig_combined = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Pump Uptime %', 'Energy Cost (R/m³)', 'SANS 241 Compliance %', 'Customer Satisfaction'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Add traces
    fig_combined.add_trace(
        go.Scatter(x=df_filtered['date'], y=df_filtered['pump_uptime'], 
                  name='Pump Uptime', line=dict(color='#1e3a8a')),
        row=1, col=1
    )
    
    fig_combined.add_trace(
        go.Scatter(x=df_filtered['date'], y=df_filtered['energy_cost'], 
                  name='Energy Cost', line=dict(color='#dc2626')),
        row=1, col=2
    )
    
    fig_combined.add_trace(
        go.Scatter(x=df_filtered['date'], y=df_filtered['compliance'], 
                  name='Compliance', line=dict(color='#059669')),
        row=2, col=1
    )
    
    fig_combined.add_trace(
        go.Scatter(x=df_filtered['date'], y=df_filtered['csat'], 
                  name='CSAT', line=dict(color='#7c3aed')),
        row=2, col=2
    )
    
    fig_combined.update_layout(height=600, title_text="Operational Performance Dashboard")
    st.plotly_chart(fig_combined, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 2: Geo Intelligence
with tab2:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.markdown("## 🗺️ Geographic Intelligence & Field Operations")
    
    # Map filters
    col1, col2, col3 = st.columns(3)
    with col1:
        incident_filter = st.selectbox("Filter by Incident Type", 
                                     ['All', 'pipe_burst', 'pump_outage', 'refill_station'])
    with col2:
        severity_filter = st.selectbox("Filter by Severity", 
                                     ['All', 'High', 'Medium', 'Low'])
    with col3:
        days_filter = st.slider("Show incidents from last N days", 1, 30, 7)
    
    # Filter geo data
    df_geo_filtered = df_geo.copy()
    
    if incident_filter != 'All':
        df_geo_filtered = df_geo_filtered[df_geo_filtered['type'] == incident_filter]
    
    if severity_filter != 'All':
        df_geo_filtered = df_geo_filtered[df_geo_filtered['severity'] == severity_filter]
    
    # Filter by days
    cutoff_date = datetime.now() - timedelta(days=days_filter)
    df_geo_filtered = df_geo_filtered[df_geo_filtered['timestamp'] >= cutoff_date]
    
    # Create color mapping
    color_map = {
        'pipe_burst': '#dc2626',
        'pump_outage': '#d97706', 
        'refill_station': '#059669'
    }
    
    size_map = {
        'High': 15,
        'Medium': 10,
        'Low': 7
    }
    
    df_geo_filtered['color'] = df_geo_filtered['type'].map(color_map)
    df_geo_filtered['size'] = df_geo_filtered['severity'].map(size_map)
    
    # Create map
    if not df_geo_filtered.empty:
        fig_map = px.scatter_mapbox(df_geo_filtered, 
                                   lat="lat", lon="lon", 
                                   color="type",
                                   size="size",
                                   hover_data=['city', 'severity', 'timestamp'],
                                   color_discrete_map=color_map,
                                   mapbox_style="open-street-map",
                                   zoom=5,
                                   center={"lat": -28.5, "lon": 24.5},
                                   title="Manzi Water Infrastructure Status Map")
        
        fig_map.update_layout(height=600)
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info("No incidents found for the selected filters.")
    
    # Incident summary
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Incident Summary")
        incident_counts = df_geo_filtered['type'].value_counts()
        fig_pie = px.pie(values=incident_counts.values, names=incident_counts.index,
                        title="Incident Distribution",
                        color_discrete_sequence=['#1e3a8a', '#059669', '#d97706'])
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.markdown("### 🚨 Critical Alerts")
        critical_incidents = df_geo_filtered[df_geo_filtered['severity'] == 'High']
        
        if not critical_incidents.empty:
            for _, incident in critical_incidents.head(5).iterrows():
                status_color = "status-red" if incident['severity'] == 'High' else "status-yellow"
                st.markdown(f"""
                <div class="kpi-card">
                    <strong>{incident['type'].replace('_', ' ').title()}</strong> - 
                    <span class="{status_color}">{incident['severity']}</span><br>
                    📍 {incident['city']}<br>
                    🕐 {incident['timestamp'].strftime('%Y-%m-%d %H:%M')}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("No critical incidents in the selected timeframe!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 3: AI Analytics
with tab3:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.markdown("## 🤖 AI-Powered Analytics & Forecasting")
    
    # AI Model Status
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="kpi-card">
            <p class="kpi-value status-green">94.2%</p>
            <p class="kpi-label">Leakage Prediction Accuracy</p>
            <p class="metric-annotation">Random Forest Model</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="kpi-card">
            <p class="kpi-value status-green">91.8%</p>
            <p class="kpi-label">Demand Forecast Accuracy</p>
            <p class="metric-annotation">LSTM Neural Network</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="kpi-card">
            <p class="kpi-value status-green">Online</p>
            <p class="kpi-label">AI Model Status</p>
            <p class="metric-annotation">Last updated: 2h ago</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Forecasting section
    st.markdown("### 📈 Predictive Analytics")
    
    # Generate forecast data
    future_dates = pd.date_range(start=df_filtered['date'].max(), periods=30, freq='D')[1:]
    
    # Leakage forecast
    col1, col2 = st.columns(2)
    
    with col1:
        # Generate mock leakage forecast
        current_leakage = df_filtered['leakage_rate'].iloc[-1]
        forecast_leakage = []
        
        for i in range(30):
            # Simulate improving trend with some noise
            predicted = current_leakage - (i * 0.05) + np.random.normal(0, 0.5)
            forecast_leakage.append(max(10, predicted))
        
        fig_leakage_forecast = go.Figure()
        
        # Historical data
        fig_leakage_forecast.add_trace(go.Scatter(
            x=df_filtered['date'][-30:], 
            y=df_filtered['leakage_rate'][-30:],
            mode='lines',
            name='Historical',
            line=dict(color='#1e3a8a')
        ))
        
        # Forecast
        fig_leakage_forecast.add_trace(go.Scatter(
            x=future_dates, 
            y=forecast_leakage,
            mode='lines',
            name='AI Forecast',
            line=dict(color='#059669', dash='dash')
        ))
        
        fig_leakage_forecast.update_layout(
            title='Leakage Rate Forecast (30 days)',
            xaxis_title='Date',
            yaxis_title='Leakage Rate (%)',
            height=400
        )
        
        st.plotly_chart(fig_leakage_forecast, use_container_width=True)
    
    with col2:
        # Water demand forecast
        base_demand = 1000000  # Base demand in liters
        forecast_demand = []
        
        for i in range(30):
            # Simulate seasonal demand with growth
            seasonal_factor = 1 + 0.2 * np.sin(2 * np.pi * i / 365)
            predicted = base_demand * seasonal_factor * (1 + np.random.normal(0, 0.1))
            forecast_demand.append(predicted)
        
        fig_demand_forecast = go.Figure()
        
        # Generate historical demand
        historical_demand = [base_demand * (1 + 0.2 * np.sin(2 * np.pi * i / 365)) 
                           for i in range(-30, 0)]
        
        fig_demand_forecast.add_trace(go.Scatter(
            x=df_filtered['date'][-30:], 
            y=historical_demand,
            mode='lines',
            name='Historical',
            line=dict(color='#1e3a8a')
        ))
        
        fig_demand_forecast.add_trace(go.Scatter(
            x=future_dates, 
            y=forecast_demand,
            mode='lines',
            name='AI Forecast',
            line=dict(color='#059669', dash='dash')
        ))
        
        fig_demand_forecast.update_layout(
            title='Water Demand Forecast (30 days)',
            xaxis_title='Date',
            yaxis_title='Daily Demand (Liters)',
            height=400
        )
        
        st.plotly_chart(fig_demand_forecast, use_container_width=True)
    
    # AI Insights
    st.markdown("### 🧠 AI Insights & Recommendations")
    
    insights = [
        {
            "title": "Predictive Maintenance Alert",
            "content": "Pump Station #7 shows 78% probability of failure in next 14 days based on vi
