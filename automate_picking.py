import xmlrpc.client

# === Replace these with your Odoo cloud info ===
url = "" #URL of Odoo cloud instance
db = "" # Odoo database name
username = "" # Odoo username or login name, usually an email address
password = ""  # Password to login

# === XML-RPC Endpoints ===
common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})

if not uid:
    raise Exception("Authentication failed. Check your credentials.")

models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

# === Fetch Product ID ===
product_name = "Pens"
product_ids = models.execute_kw(db, uid, password,
    'product.product', 'search',
    [[['name', '=', product_name]]], {'limit': 1})

if not product_ids:
    raise Exception("Product not found.")

product_id = product_ids[0]

# === Fetch Operation Type ID ===
operation_name = "Delivery to HSE" #literally the operation type name in Odoo
operation_ids = models.execute_kw(db, uid, password,
    'stock.picking.type', 'search',
    [[['name', '=', operation_name]]], {'limit': 1})

if not operation_ids:
    raise Exception("Operation type not found.")

picking_type_id = operation_ids[0]

# === Create Picking (Inventory Move) ===
picking_id = models.execute_kw(db, uid, password, 'stock.picking', 'create', [{
    'partner_id': False,  # Optional: Customer/recipient
    'picking_type_id': picking_type_id,
    'location_id': 26,         # Usually your source location ID (change as needed)
    'location_dest_id': 39,    # Destination location ID (change as needed)
    'move_ids_without_package': [(0, 0, {
        'name': f'Delivery of {product_name}',
        'product_id': product_id,
        'product_uom_qty': 10,
        'product_uom': 1,  # Check your UOM ID
        'location_id': 26,
        'location_dest_id': 39,
    })]
}])

print(f"✅ Picking Created: ID {picking_id}")

# === Confirm the picking ===
models.execute_kw(db, uid, password, 'stock.picking', 'action_confirm', [[picking_id]])
print("✅ Picking Confirmed")

# === Optional: Mark as Done ===
# models.execute_kw(db, uid, password, 'stock.picking', 'action_done', [[picking_id]])
models.execute_kw(db, uid, password, 'stock.picking', 'button_validate', [[picking_id]])
print("✅ Picking Completed")
