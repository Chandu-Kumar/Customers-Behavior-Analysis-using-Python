import pandas as pd
import numpy as np
df = pd.read_excel(r"C:\Users\Chandu Kumar\Downloads\customer_shopping_behavior.xlsx")

#_____________________$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#--------#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$_________________________
#_____________________$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$_________________________
print(df.head())
print(df.tail())

print(len(df))  #total no. of rows
print(df.shape)

print(df.describe())
print(df.describe(include="all"))

df.info()

print(df.isnull().sum())

#Data Cleaning
print(df.head())
print(df['Item Purchased'].unique())
print(df['Item Purchased'].nunique())
print(df['Category'].unique())
print(df['Category'].nunique())
print(df.groupby('Category')['Item Purchased'].unique())
print(df.groupby('Category')['Item Purchased'].nunique())
pd.set_option('display.max_colwidth',None)
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)
print(df.groupby('Category')['Item Purchased'].unique())
correct_mapping = {
    "Sunglasses": "Accessories",
    "Gloves": "Accessories",
    "Jewelry": "Accessories",
    "Hat": "Accessories",
    "Handbag": "Accessories",
    "Backpack": "Accessories",
    "Belt": "Accessories",
    "Scarf": "Accessories",
    "Bag": "Accessories",

    "T-shirt": "Clothing",
    "Shirt": "Clothing",
    "Shorts": "Clothing",
    "Hoodie": "Clothing",
    "Pants": "Clothing",
    "Socks": "Clothing",
    "Jeans": "Clothing",
    "Blouse": "Clothing",
    "Skirt": "Clothing",
    "Sweater": "Clothing",
    "Dress": "Clothing",

    "Laptop": "Electronics",
    "Phone": "Electronics",
    "Headphones": "Electronics",
    "Watch":"Electronics",

    "Shoes": "Footwear",
    "Sandals": "Footwear",
    "Sneakers": "Footwear",
    "Boots": "Footwear",

    "Coat": "Outerwear",
    "Jacket": "Outerwear",

}
df["Category"]=df["Item Purchased"].map(correct_mapping)
print(df.groupby('Category')['Item Purchased'].unique())
print(df.groupby('Category')['Item Purchased'].nunique())

#Treating the null values
print(df.isnull().sum())
print(df['Size'].unique())
print(df.groupby('Category')['Size'].unique())

print(df.groupby('Item Purchased')['Size'].unique())

#treating null values or replacing all values in electronic category
df.loc[df['Category']=='Electronics','Size']="Not applicable"
print(df.groupby('Category')['Size'].unique())
#treating null values or replacing all values in accessories category
df.loc[df['Category']=='Accessories','Size']="Free Size"
print(df.groupby('Category')['Size'].unique())

#treating null values or replacing all values in footwear category
df.loc[df['Category']=='Footwear','Size']="not available"
print(df.groupby('Category')['Size'].unique())

#treating null values or replacing all values in clothing category
df.loc[(df['Category']=='Clothing')&(df['Size'].isnull()),'Size']=df[df['Category']=='Clothing']['Size'].mode()[0]
print(df.groupby('Category')['Size'].unique())

print(df.isnull().sum())

print(df['Review Rating'].mean())
print(df['Review Rating'].median())
print(df['Review Rating'].mode())
print(df.groupby("Item Purchased")["Review Rating"].mean())
#filling null value of Review Rating with the mean of each Items Purchased
df['Review Rating'] = df['Review Rating'].fillna(df.groupby('Item Purchased')['Review Rating'].transform("mean"))
print(df.head())
#df['Review Rating']=df["Review Rating"].round(2)
print(df.isnull().sum())
#filling previous purchase with zero(0)
df['Previous Purchases'] = df['Previous Purchases'].fillna(0)
print(df.isnull().sum())
#filling Purchased Amount columun
print(df.groupby("Item Purchased")['Purchase Amount (USD)'].mean())
df['Purchase Amount (USD)'] = df['Purchase Amount (USD)'].fillna(df.groupby("Item Purchased")['Purchase Amount (USD)'].transform("mean"))
print(df.isnull().sum())

#Checking duplicates
print(df.duplicated().sum())
print(df[df.duplicated()])
print(df[df['Customer ID']==974])
print(len(df))
#dropping duplicated values
df = df.drop_duplicates(subset=['Customer ID'],keep='first')
print(len(df))

#Renaming the Headers
df.columns = df.columns.str.replace(" ","_")
print(df.head())
df.columns = df.columns.str.lower()
print(df.head())
#Replacing purchase_amount_(usd) to purchase_amount
df = df.rename(columns = {"purchase_amount_(usd)":"purchase_amount"})

print(df.columns)

#--Bussiness Insights Questions
#--------------------------------------------------------
#--1. Which category generates highest revenue?
# Group by + sum + sort
revenue_by_category = (
    df.groupby("category")["purchase_amount"]
      .sum()
      .round(2)
      .sort_values(ascending=False)
      .reset_index(name="highest_revenue")
)

print(revenue_by_category)
#-- ? Bussiness Problems:- Company does not know which category contributes most to revenue
#-- Impact:-
		#--Helps prioritize high-performing categories
		#--Optimizes inventory planning
		#--Improves marketing ROI


#--2. Are discounts actually increasing purchase value?


# Group by + aggregation
revenue_with_discount = df.groupby("discount_applied").agg(
    total_revenue=("purchase_amount", "sum"),
    avg_revenue=("purchase_amount", "mean")
)

# Round values
revenue_with_discount = revenue_with_discount.round(2)

print(revenue_with_discount)

#--? Bussiness Problems:- Discounts may reduce profit without increasing sales.

#--Impact:-
		#--Identify effectiveness of discounts
		#--Reduce unnecessary discount costs
		#--Improve profit margins


#--3. What is the total revenue generated by male and female customer ?

# Group by gender + sum + sort
revenue_by_gender = (
    df.groupby("gender")["purchase_amount"]
      .sum()
      .round(2)
      .sort_values(ascending=False)
      .reset_index(name="highest_revenue")
)

print(revenue_by_gender)

#--? Bussiness Problem:- Lack of understanding of revenue contribution by gender segments.
#--Impact:-
		#--Helps design targeted marketing campaigns
		#--Improves customer segmentation strategy
		#--Enhances personalization efforts


#--4. Which customer used a discount but still spent more than the average purchase amount ?


# Step 1: average purchase निकालो
avg_value = df["purchase_amount"].mean()

# Step 2: filter apply karo
result = (
    df[(df["discount_applied"] == "Yes") & 
       (df["purchase_amount"] > avg_value)]
    .sort_values(by="purchase_amount", ascending=False)
    [["customer_id", "purchase_amount", "discount_applied"]]
    .head(10)
)
# Step 3: top 10 rows


print(result)

#--? Bussiness Problem:- Company cannot identify high-spending customers who are also discount users.

#--Impact:-
		#--Identifies premium discount-sensitive customers
		#--Enables targeted discount campaigns
		#--Improves customer retenttion and revenue

#--5. Which are the top/bottom 5 products with the highest average review rating.
# Highest rated items (Top 5)
top_rated = (
    df.groupby("item_purchased")["review_rating"]
      .mean()
      .round(2)
      .sort_values(ascending=False)
      .head(5)
      .reset_index(name="avg_ratings")
)
print(top_rated)
# Lowest rated items (Top 5)
low_rated = (
    df.groupby("item_purchased")["review_rating"]
      .mean()
      .round(2)
      .sort_values(ascending=True)
      .head(5)
      .reset_index(name="avg_ratings")
)

print(low_rated)

#--? Bussiness Problems:- No visibility into product performance based on customer satisfaction.

#--Impact:-
#		--Promotes high-performing products
#		--Improves low-rated products
#		--Enhances custtomer experience

#--6. Average purchase: Standard vs Express shipping
avg_purchase_by_shipping_type = (
    df.groupby("shipping_type").agg(
        order_placed=("customer_id", "nunique"),   # count distinct
        avg_purchase=("purchase_amount", "mean"),
        revenue=("purchase_amount", "sum")
    )
    .round(2)
    .reset_index()
)

print(avg_purchase_by_shipping_type)

#--? Bussiness Proble:- Unclear if faster shipping leads to higher spending
#--Impact
#		--Helps optimize shipping pricing strategy
#		--Encourage premium shipping adoption
#		--Increase average order value



##############################################-------------------------VISUALIZATION----------------------################################################



import matplotlib.pyplot as plt
plt.figure(figsize=(8,5))
plt.style.use('seaborn-v0_8')
#plt.style.use('ggplot')
plt.bar(revenue_by_category["category"], revenue_by_category["highest_revenue"],color = ['#03045E', '#0077B6', '#00B4D8', '#90E0EF', '#CAF0F8'])
plt.xticks(rotation=45)
plt.xlabel("Category")
plt.ylabel("Revenue")
plt.title("Revenue by Category",fontweight='bold',fontsize=14)

plt.show()

#--2. Are discounts actually increasing purchase value?
#plt.figure(figsize=(5,8))
plt.style.use('seaborn-v0_8')
revenue_with_discount[["total_revenue"]].plot(kind="bar", title="Total Revenue",color=["#2A9D8F", "#E76F51"])
#plt.figure(figsize=(5,8))

revenue_with_discount[["avg_revenue"]].plot(kind="bar", title="Average Revenue",color=["#264653", "#F4A261"])
plt.show()


#--3.revenue contribution by gender segments?


plt.pie(
    revenue_by_gender["highest_revenue"],
    labels=revenue_by_gender["gender"],
    autopct="%1.1f%%",
    colors=["#2A9D8F", "#E76F51", "#264653"],
    
)

plt.title("Revenue Contribution by Gender", fontweight='bold')
plt.axis('equal')

plt.show()

#--5. Which are the top/bottom 5 products with the highest average review rating.


plt.style.use('seaborn-v0_8')

# Top rated
plt.figure(figsize=(6,4))
plt.bar(
    top_rated["item_purchased"],
    top_rated["avg_ratings"],
    color="#2A9D8F"
)
plt.title("Top 5 Highest Rated Products", fontweight='bold')
plt.ylabel("Average Rating")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# Lowest rated
plt.figure(figsize=(6,4))           
plt.bar(
    low_rated["item_purchased"],
    low_rated["avg_ratings"],
    color="#E76F51"
)
plt.title("Top 5 Lowest Rated Products", fontweight='bold')
plt.ylabel("Average Rating")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#--6. Average purchase: Standard vs Express shipping

import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8')

# 1. Average Purchase
plt.figure(figsize=(6,4))
plt.bar(
    avg_purchase_by_shipping_type["shipping_type"],
    avg_purchase_by_shipping_type["avg_purchase"],
    color="#2A9D8F"
)
plt.title("Average Purchase: Standard vs Express", fontweight='bold')
plt.xlabel("Shipping Type")
plt.ylabel("Avg Purchase")
plt.tight_layout()
plt.show()


# 2. Revenue Comparison
plt.figure(figsize=(6,4))
plt.bar(
    avg_purchase_by_shipping_type["shipping_type"],
    avg_purchase_by_shipping_type["revenue"],
    color="#264653"
)
plt.title("Total Revenue by Shipping Type", fontweight='bold')
plt.ylabel("Revenue")
plt.tight_layout()
plt.show()


# 3. Orders Comparison
plt.figure(figsize=(6,4))
plt.bar(
    avg_purchase_by_shipping_type["shipping_type"],
    avg_purchase_by_shipping_type["order_placed"],
    color="#E76F51"
)
plt.title("Orders by Shipping Type", fontweight='bold')
plt.ylabel("Number of Orders")
plt.tight_layout()
plt.show()

import seaborn as sns


corr = df.corr(numeric_only=True)

plt.figure(figsize=(8,5))
sns.heatmap(
    corr,
    annot=True,
    cmap='coolwarm',
    fmt=".2f",        # values 2 decimal me
    linewidths=0.5    # thodi spacing
)

plt.title("Correlation Heatmap", fontweight='bold')
plt.xticks(rotation=45)
plt.yticks(rotation=0)

plt.tight_layout()
plt.show()

plt.style.use('seaborn-v0_8')

plt.figure(figsize=(6,4))
plt.scatter(
    df['purchase_amount'],
    df['review_rating'],
    color="#2A9D8F",
    alpha=0.6   # transparency (overlapping clear dikhega)
)

plt.xlabel("Purchase Amount")
plt.ylabel("Review Rating")
plt.title("Purchase vs Review Rating", fontweight='bold')

plt.tight_layout()
plt.show()

