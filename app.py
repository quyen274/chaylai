import streamlit as st
import pandas as pd
import numpy as np
import json

# Load dữ liệu
df = pd.read_csv('current_day_sales.csv')
df['Time'] = pd.to_datetime(df['Time'])

# Chuẩn bị dữ liệu JSON cho JavaScript
grouped = df.groupby(['Time', 'Platform']).sum().unstack(fill_value=0)
data_json = grouped.reset_index().to_json(orient='records')

# Streamlit Title
st.title('Biểu Đồ Doanh Số 7 Ngày')
st.write("Sử dụng JavaScript để zoom và trượt biểu đồ.")

# HTML + JavaScript cho Chart.js
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-zoom"></script>
</head>
<body>
    <canvas id="myChart" width="800" height="400"></canvas>
    <script>
        const ctx = document.getElementById('myChart').getContext('2d');
        const data = {data_json};

        const labels = data.map(row => row.Time);
        const datasets = Object.keys(data[0])
            .filter(key => key !== 'Time')
            .map(platform => ({
                label: platform,
                data: data.map(row => row[platform] || 0),
                borderColor: '#' + Math.floor(Math.random()*16777215).toString(16),
                fill: false
            }));

        const config = {{
            type: 'line',
            data: {{
                labels: labels,
                datasets: datasets
            }},
            options: {{
                responsive: true,
                plugins: {{
                    zoom: {{
                        zoom: {{
                            enabled: true,
                            mode: 'x',
                            drag: true
                        }},
                        pan: {{
                            enabled: true,
                            mode: 'x'
                        }}
                    }}
                }},
                scales: {{
                    x: {{
                        display: true,
                        title: {{
                            display: true,
                            text: 'Thời Gian'
                        }}
                    }},
                    y: {{
                        display: true,
                        title: {{
                            display: true,
                            text: 'Doanh Số'
                        }}
                    }}
                }}
            }}
        }};
        new Chart(ctx, config);
    </script>
</body>
</html>
"""

# Hiển thị biểu đồ
st.components.v1.html(html_code, height=500)
