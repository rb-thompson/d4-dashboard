from django.shortcuts import render
from .forms import SessionForm
from .models import Session
import plotly.express as px
import pandas as pd

def dashboard(request):
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            # Save paragon_points as logged, no cap
            form.save()
    else:
        form = SessionForm()
    
    # Fetch session data
    sessions = Session.objects.all().values()
    df = pd.DataFrame(sessions)
    
    # Initialize metrics and charts
    metrics = {}
    trend_fig = fun_fig = None
    no_data_message = "No data available. Start logging your Diablo IV sessions to see your progress!"

    if not df.empty:
        # Calculate estimated DPS, handling potential NaN
        df['estimated_dps'] = df.apply(
            lambda row: 1000 * (1 + (row['skill_ranks'] or 0) * 0.1) * \
                       (1 + (row['intelligence'] or 0) / 1000) * \
                       (1 + (row['lightning_damage'] or 0) / 100) * \
                       (row['attack_speed'] or 1) * \
                       (1 + (row['crit_chance'] or 0) * (row['crit_damage'] or 0) / 100) if pd.notna(row['intelligence']) else 0,
            axis=1
        )
        # Update database
        for idx, row in df.iterrows():
            Session.objects.filter(id=row['id']).update(estimated_dps=row['estimated_dps'])
        
        # Metrics with fallback for NaN
        metrics = {
            'mythic_count': df['mythics_dropped'].sum(),
            'mythic_drop_rate': (df['mythics_dropped'].mean() / df['session_length'].mean() * 60) if df['session_length'].mean() else 0,  # Drops/hour
            'avg_dps': df['estimated_dps'].mean() if pd.notna(df['estimated_dps']).all() else 0,
            'avg_crit': df['crit_chance'].mean() if pd.notna(df['crit_chance']).all() else 0,
            'paragon_total': df['paragon_points'].iloc[-1] if not df.empty else 0,  # Latest value
            'avg_fun': df['fun_score'].mean() if pd.notna(df['fun_score']).all() else 0,
            'total_sessions': len(df)  # Total number of logged sessions
        }
        
        # Style and create Plotly charts
        if len(df) > 0:
            trend_fig = px.line(df, x='date', y='estimated_dps', title='Estimated DPS Trend')
            trend_fig.update_traces(line=dict(color="#ffaa00"))
            trend_fig.update_layout(
                plot_bgcolor='#111827',
                paper_bgcolor='#111827',
                title_font_color='#00ff41',
                font_color='#00ff41',
                title_font_size=18,
                xaxis_title="Session Date",
                yaxis_title="DPS (Damage Per Second)",
                xaxis_title_font_color='#ba53ff',
                yaxis_title_font_color='#ba53ff'
            )
            trend_fig.update_layout(showlegend=False)
            trend_fig.update_xaxes(showgrid=True, gridcolor='#1e293b')
            trend_fig.update_yaxes(showgrid=True, gridcolor='#1e293b')

        if len(df) > 0 and df['session_length'].notna().any() and df['fun_score'].notna().any():
            fun_fig = px.scatter(df, x='session_length', y='fun_score', size='mythics_dropped',
                               title='Fun vs Session Length', text='activity_type')
            fun_fig.update_traces(marker=dict(color='#ffbf00', size=10, sizemode='diameter'),
                                textposition="top center")
            fun_fig.update_layout(
                plot_bgcolor='#111827',
                paper_bgcolor='#111827',
                title_font_color='#00ff41',
                font_color='#00ff41',
                title_font_size=18,
                xaxis_title="Session Duration (minutes)",
                yaxis_title="Fun Score (1-10)",
                xaxis_title_font_color='#ba53ff',
                yaxis_title_font_color='#ba53ff'
            )
            fun_fig.update_layout(showlegend=False)
            fun_fig.update_xaxes(showgrid=True, gridcolor='#1e293b')
            fun_fig.update_yaxes(showgrid=True, gridcolor='#1e293b')
    else:
        # No data case for charts
        trend_fig = px.scatter(title='Estimated DPS Trend (No Data)')
        trend_fig.update_layout(
            plot_bgcolor='#111827',
            paper_bgcolor='#111827',
            title_font_color='#00ff41',
            font_color='#00ff41',
            title_font_size=18
        )
        fun_fig = px.scatter(title='Fun vs Session Length (No Data)')
        fun_fig.update_layout(
            plot_bgcolor='#111827',
            paper_bgcolor='#111827',
            title_font_color='#00ff41',
            font_color='#00ff41',
            title_font_size=18
        )
        # No data case for metrics
        metrics = {
            'mythic_count': 'No Data',
            'mythic_drop_rate': 'No Data',
            'avg_dps': 'No Data',
            'avg_crit': 'No Data',
            'paragon_total': 'No Data',
            'avg_fun': 'No Data',
            'total_sessions': 'No Data'
        }

    return render(request, 'tracker/dashboard.html', {
        'form': form,
        'metrics': metrics,
        'trend_fig': trend_fig.to_html() if trend_fig else '',
        'fun_fig': fun_fig.to_html() if fun_fig else '',
        'no_data_message': no_data_message
    })