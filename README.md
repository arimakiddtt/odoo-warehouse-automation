# 🏗️ Odoo Warehouse Automation (XML-RPC)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Odoo](https://img.shields.io/badge/Odoo-Inventory%20Module-purple?logo=odoo)


This project demonstrates how to automate **warehouse inventory operations** in the Odoo ERP system using **Python** and **XML-RPC**. It includes a working example of creating and confirming a stock picking (delivery order) programmatically.

Ideal for use cases like:
- 🔄 Automating repetitive logistics workflows
- 🧠 Building AI-driven or voice-enabled ERP interactions
- 🧪 Testing integrations with Odoo Inventory

---

## ⚙️ Features

- ✅ Connects to any Odoo instance (v13+)
- ✅ Searches for products and operation types
- ✅ Creates warehouse stock pickings (Inventory Moves)
- ✅ Confirms and validates the picking
- 🚀 Future-ready for AI/voice "text-to-action" layers

---

## 📌 Required Setup

At the top of the script (`automate_picking.py`), **update these values**:

```python
url = ""         # Your Odoo instance URL
db = ""          # Your Odoo DB name
username = ""    # Your Odoo login (email)
password = ""    # Your password

product_name = "Pens"
operation_name = "Delivery to HSE"    # Must match an Operation Type in Odoo exactly
location_id = 26                      # Source location ID
location_dest_id = 39                 # Destination location ID
product_uom = 1                       # Unit of Measure ID (check your UOMs)
product_uom_qty = 10                  # Quantity to deliver

📎 Where do I get these values?
You can retrieve these values directly from your Odoo interface or database.
In a future update, I’ll show how to use SQL queries to fetch them programmatically.

🚨 For now, it's your responsibility to collect these values based on your Odoo environment.

🚀 How It Works
The script connects to the Odoo Inventory module and performs:

Authentication via XML-RPC

Product lookup by name

Picking Type lookup (e.g., Delivery to HSE)

Creates a stock.picking with move lines

Confirms and validates the operation
