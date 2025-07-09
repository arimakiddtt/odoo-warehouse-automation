

import xmlrpc.client

# === Replace these with your Odoo cloud info ===
url = "" #URL of Odoo cloud instance
db = "" # Odoo database name
username = "" # Odoo username or login name, usually an email address
password = ""  # Password to login

# === XML-RPC Authentication ===
common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})

if not uid:
    raise Exception("Authentication failed. Check your credentials.")

models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

# === Product Resolver ===
def resolve_product_id(display_name):
    """Handles both simple and variant products"""
    if "(" in display_name and display_name.endswith(")"):
        template_name = display_name.split(" (")[0].strip()
        attribute_value = display_name.split(" (")[1].rstrip(")").strip()
    else:
        template_name = display_name.strip()
        attribute_value = None

    # Try finding the template
    template_id = models.execute_kw(db, uid, password,
        'product.template', 'search',
        [[['name', '=', template_name]]], {'limit': 1})

    if not template_id:
        raise Exception(f"Product template '{template_name}' not found")

    # Find variants
    variant_ids = models.execute_kw(db, uid, password,
        'product.product', 'search',
        [[['product_tmpl_id', '=', template_id[0]]]])

    if not variant_ids:
        raise Exception(f"No variants found for template '{template_name}'")

    # Simple product (no variant name provided)
    if attribute_value is None:
        return variant_ids[0]

    # Complex variant: scan attribute values
    variants = models.execute_kw(db, uid, password,
        'product.product', 'read',
        [variant_ids, ['id', 'product_template_attribute_value_ids']])

    for variant in variants:
        attr_values = models.execute_kw(db, uid, password,
            'product.template.attribute.value', 'read',
            [variant['product_template_attribute_value_ids'], ['name']])
        
        if any(attribute_value.lower() in attr['name'].lower() for attr in attr_values):
            return variant['id']

    raise Exception(f"No variant found matching '{display_name}'")

# === INPUT: Just change this to match your needs ===
product_display_name = "Coffee Mug (White)"  # or "Pens"
operation_name = "Delivery to HSE"

# === Resolve Product ID ===
product_id = resolve_product_id(product_display_name)

# === Fetch Operation Type ID ===
operation_ids = models.execute_kw(db, uid, password,
    'stock.picking.type', 'search',
    [[['name', '=', operation_name]]], {'limit': 1})

if not operation_ids:
    raise Exception("Operation type not found.")
picking_type_id = operation_ids[0]

# === Create Inventory Movement ===
picking_id = models.execute_kw(db, uid, password, 'stock.picking', 'create', [{
    'partner_id': False,
    'picking_type_id': picking_type_id,
    'location_id': 26,
    'location_dest_id': 39,
    'move_ids_without_package': [(0, 0, {
        'name': f'Delivery of {product_display_name}',
        'product_id': product_id,
        'product_uom_qty': 10,
        'product_uom': 1,
        'location_id': 26,
        'location_dest_id': 39,
    })]
}])

print(f"✅ Picking Created: ID {picking_id}")

# === Confirm + Validate ===
models.execute_kw(db, uid, password, 'stock.picking', 'action_confirm', [[picking_id]])
print("✅ Picking Confirmed")

models.execute_kw(db, uid, password, 'stock.picking', 'button_validate', [[picking_id]])
print("✅ Picking Completed")
