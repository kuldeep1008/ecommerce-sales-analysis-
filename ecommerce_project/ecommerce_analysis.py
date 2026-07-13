
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import warnings
warnings.filterwarnings('ignore')

# ── STEP 1: LOAD DATA ────────────────────────────────────
df = pd.read_csv('ecommerce_data.csv', parse_dates=['InvoiceDate'])

print("=== RAW DATA ===")
print(f"Shape       : {df.shape}")
print(f"Columns     : {df.columns.tolist()}")
print(f"Missing     :\n{df.isnull().sum()}\n")

# ── STEP 2: CLEAN DATA ───────────────────────────────────
df = df.dropna(subset=['CustomerID'])   # remove missing customers
df = df[df['UnitPrice'] > 0]           # remove zero-price records
df = df[df['Quantity']  > 0]           # remove zero-quantity records
df['Revenue']   = df['Quantity'] * df['UnitPrice']
df['Month']     = df['InvoiceDate'].dt.month
df['MonthName'] = df['InvoiceDate'].dt.strftime('%b')

print("=== CLEANED DATA ===")
print(f"Shape after cleaning : {df.shape}")
print(f"Total Revenue        : £{df['Revenue'].sum():,.2f}\n")

# ── STEP 3: ANSWER BUSINESS QUESTIONS ────────────────────

# Q1: Revenue by Country
rev_country = df.groupby('Country')['Revenue'].sum().sort_values(ascending=False).reset_index()
print("Q1 — Revenue by Country:\n", rev_country.to_string(index=False), "\n")

# Q2: Top Products
top_products = df.groupby('Description')['Revenue'].sum().sort_values(ascending=False).reset_index()
print("Q2 — Top Products:\n", top_products.to_string(index=False), "\n")

# Q3: Monthly Revenue
monthly = df.groupby(['Month','MonthName'])['Revenue'].sum().reset_index().sort_values('Month')
print("Q3 — Monthly Revenue:\n", monthly[['MonthName','Revenue']].to_string(index=False), "\n")

# Q4: Top Customers
top_customers = df.groupby('CustomerID')['Revenue'].sum().sort_values(ascending=False).head(10).reset_index()
print("Q4 — Top 10 Customers:\n", top_customers.to_string(index=False), "\n")

# Q5: Average Order Value
aov = df.groupby('InvoiceNo')['Revenue'].sum().mean()
print(f"Q5 — Average Order Value: £{aov:,.2f}")

# ── STEP 4: VISUALISE ────────────────────────────────────
plt.rcParams.update({'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.grid': True, 'grid.alpha': 0.3, 'figure.facecolor': 'white'})

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('E-Commerce Sales Analysis — 2023', fontsize=16, fontweight='bold', y=1.01)

# Chart 1
axes[0,0].barh(rev_country['Country'][::-1], rev_country['Revenue'][::-1], color='#2c5f8a')
axes[0,0].set_title('Revenue by Country', fontweight='bold')
axes[0,0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'£{x/1000:.0f}K'))

# Chart 2
axes[0,1].barh(top_products['Description'][::-1], top_products['Revenue'][::-1], color='#3d7ab5')
axes[0,1].set_title('Top Products by Revenue', fontweight='bold')
axes[0,1].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'£{x/1000:.0f}K'))

# Chart 3
axes[1,0].plot(monthly['MonthName'], monthly['Revenue'], marker='o', color='#2c5f8a', linewidth=2)
axes[1,0].set_title('Monthly Revenue Trend', fontweight='bold')
axes[1,0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'£{x/1000:.0f}K'))

# Chart 4
axes[1,1].bar(top_customers['CustomerID'], top_customers['Revenue'], color='#5a9fd4')
axes[1,1].set_title('Top 10 Customers', fontweight='bold')
axes[1,1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'£{x/1000:.0f}K'))
axes[1,1].tick_params(axis='x', rotation=30)

plt.tight_layout()
plt.savefig('charts/ecommerce_dashboard.png', dpi=150, bbox_inches='tight')
print("\nDashboard chart saved!")
