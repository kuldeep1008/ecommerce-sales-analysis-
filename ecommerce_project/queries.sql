-- ============================================================
-- E-Commerce Sales Analysis — SQL Queries
-- Author  : Kuldeep Sharma
-- Database: MySQL
-- ============================================================

-- Create table
CREATE TABLE IF NOT EXISTS ecommerce (
    InvoiceNo   VARCHAR(20),
    StockCode   VARCHAR(20),
    Description VARCHAR(100),
    Quantity    INT,
    InvoiceDate DATETIME,
    UnitPrice   DECIMAL(10,2),
    CustomerID  VARCHAR(20),
    Country     VARCHAR(50)
);

-- Q1: Total Revenue by Country
SELECT Country,
       ROUND(SUM(Quantity * UnitPrice), 2) AS Total_Revenue
FROM ecommerce
WHERE UnitPrice > 0 AND Quantity > 0 AND CustomerID IS NOT NULL
GROUP BY Country
ORDER BY Total_Revenue DESC;

-- Q2: Top 10 Products by Revenue
SELECT Description,
       ROUND(SUM(Quantity * UnitPrice), 2) AS Revenue,
       SUM(Quantity) AS Units_Sold
FROM ecommerce
WHERE UnitPrice > 0 AND Quantity > 0
GROUP BY Description
ORDER BY Revenue DESC
LIMIT 10;

-- Q3: Monthly Revenue Trend
SELECT MONTH(InvoiceDate)  AS Month_Num,
       MONTHNAME(InvoiceDate) AS Month_Name,
       ROUND(SUM(Quantity * UnitPrice), 2) AS Monthly_Revenue
FROM ecommerce
WHERE UnitPrice > 0 AND Quantity > 0
GROUP BY MONTH(InvoiceDate), MONTHNAME(InvoiceDate)
ORDER BY Month_Num;

-- Q4: Top 10 Customers by Total Spend
SELECT CustomerID,
       COUNT(DISTINCT InvoiceNo) AS Total_Orders,
       ROUND(SUM(Quantity * UnitPrice), 2) AS Total_Spent
FROM ecommerce
WHERE CustomerID IS NOT NULL AND UnitPrice > 0
GROUP BY CustomerID
ORDER BY Total_Spent DESC
LIMIT 10;

-- Q5: Average Order Value
SELECT ROUND(AVG(order_total), 2) AS Avg_Order_Value
FROM (
    SELECT InvoiceNo, SUM(Quantity * UnitPrice) AS order_total
    FROM ecommerce
    WHERE UnitPrice > 0 AND Quantity > 0
    GROUP BY InvoiceNo
) t;

-- Q6: Revenue by Country using CTE
WITH country_revenue AS (
    SELECT Country,
           ROUND(SUM(Quantity * UnitPrice), 2) AS Revenue
    FROM ecommerce
    WHERE UnitPrice > 0 AND CustomerID IS NOT NULL
    GROUP BY Country
),
total AS (
    SELECT SUM(Revenue) AS Grand_Total FROM country_revenue
)
SELECT cr.Country, cr.Revenue,
       ROUND(cr.Revenue / t.Grand_Total * 100, 1) AS Pct_Share
FROM country_revenue cr, total t
ORDER BY cr.Revenue DESC;

-- Q7: Rank customers using Window Function
SELECT CustomerID,
       ROUND(SUM(Quantity * UnitPrice), 2) AS Total_Spent,
       RANK() OVER (ORDER BY SUM(Quantity * UnitPrice) DESC) AS Customer_Rank
FROM ecommerce
WHERE CustomerID IS NOT NULL AND UnitPrice > 0
GROUP BY CustomerID
ORDER BY Customer_Rank
LIMIT 10;
