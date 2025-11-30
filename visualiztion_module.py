import csv
import os
from collections import defaultdict
import plotly.graph_objects as go

DATA_FILE = 'expenses.csv'

def load_expenses():
    """讀取 expenses.csv 並依類別加總金額"""
    if not os.path.exists(DATA_FILE):
        print("找不到 expenses.csv，請先執行輸入模組新增資料。")
        return None
    category_totals = defaultdict(float)
    with open(DATA_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                amount = float(row['Amount'])
                category = row['Category']
                category_totals[category] += amount
            except:
                continue
    return category_totals

def plot_interactive_3d_pie(category_totals):
    """3D 錯位陰影版 + 自訂懸停文字 + RWD響應式設計"""
    if not category_totals:
        print("沒有資料可畫圖")
        return

    categories = list(category_totals.keys())
    amounts = list(category_totals.values())
    num_categories = len(categories)

    pastel_colors = [
        "rgb(255, 204, 204)", "rgb(255, 229, 204)", "rgb(255, 255, 204)",
        "rgb(204, 255, 204)", "rgb(204, 229, 255)", "rgb(229, 204, 255)"
    ]

    pull_config = [0.05] * num_categories

    # --- 1. 陰影層 ---
    trace_shadow = go.Pie(
        labels=categories,
        values=amounts,
        pull=pull_config,
        marker=dict(
            colors=['rgba(0, 0, 0, 0.5)'] * num_categories, 
            line=dict(width=0)
        ),
        # 使用 domain 設定相對位置 (百分比)，這對 RWD 很重要
        domain={'x': [0.02, 1.0], 'y': [0.0, 0.98]},
        hoverinfo='skip',
        textinfo='none',
        showlegend=False,
        sort=False
    )

    # --- 2. 主圖層 ---
    trace_main = go.Pie(
        labels=categories,
        values=amounts,
        pull=pull_config,
        marker=dict(
            colors=pastel_colors[:num_categories],
            line=dict(color="white", width=2),
        ),
        domain={'x': [0.0, 0.98], 'y': [0.02, 1.0]},
        
        # 自訂 Tooltip 格式
        hovertemplate=(
            "<b>種類: %{label}</b><br>" + 
            "金額: %{value}<br>" + 
            "占比: %{percent}" + 
            "<extra></extra>"
        ),
        hoverlabel=dict(
            bgcolor="white",
            font=dict(size=14, color="black"),
            bordercolor=pastel_colors[:num_categories]
        ),
        
        textinfo="label+percent",
        sort=False
    )

    fig = go.Figure(data=[trace_shadow, trace_main])

    # --- Layout 設定修改 ---
    fig.update_layout(
        title={
            'text': "Expense Tracker PieChart",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=26, family="Arial Black")
        },
        showlegend=True,
        paper_bgcolor="rgba(240,240,240,1)",
        plot_bgcolor="rgba(240,240,240,1)",
        
        # 關鍵修改 1: 移除 width/height，改用 autosize
        autosize=True,
        # 設定邊距為 0 或很小，讓圖表能盡量填滿容器
        margin=dict(l=20, r=20, t=80, b=20),
    )

    # 關鍵修改 2: 在 show 裡面加入 config 設定 responsive 為 True
    fig.show(config={'responsive': True})

def main():
    data = load_expenses()
    if data:
        plot_interactive_3d_pie(data)

if __name__ == "__main__":
    main()