/*
variable(non variant): product_name
details:
depending on the language setting of the user.
Note that your language may not be either of what is used in 
the query.  If you see multiple products, then that's a variant
which means you'll have to use another query.  The
sql query below will output non-variant products
Example: "Pens"
*/
-- Try en_GB first, then fallback to en_US
SELECT 
    pp.id AS product_id,
    COALESCE(pt.name->>'en_GB', pt.name->>'en_US') AS preferred_product_name,
    pt.uom_id
FROM 
    product_product pp
JOIN 
    product_template pt ON pp.product_tmpl_id = pt.id;
    
/*
variable(variant): product_name
The sql query below will output all the products
that are variants.  Use the value for the
full_variant_name when modifying the script 
Example:
product_name = "Coffee Mug (White)"
*/
select * from product_variant_combination;

SELECT 
    pp.id AS product_id,
    pt.name->>'en_US' AS base_name,
    STRING_AGG(pav.name->>'en_US', ', ') AS attribute_values,
    CASE 
        WHEN COUNT(pav.name) > 0 
        THEN pt.name->>'en_US' || ' (' || STRING_AGG(pav.name->>'en_US', ', ') || ')'
        ELSE pt.name->>'en_US'
    END AS full_variant_name
FROM 
    product_product pp
JOIN 
    product_template pt ON pp.product_tmpl_id = pt.id
JOIN 
    product_variant_combination pvc ON pvc.product_product_id = pp.id
JOIN 
    product_template_attribute_value ptav ON ptav.id = pvc.product_template_attribute_value_id
JOIN 
    product_attribute_value pav ON pav.id = ptav.product_attribute_value_id
WHERE 
    pt.name->>'en_US' = 'Coffee Mug'
GROUP BY 
    pp.id, pt.name;
    
/*
variable: operation_name
When you run this query you'll see JSON that wraps
the languages.  It looks like:
{"en_GB": "Delivery to HSE", "en_US": "Delivery to HSE"}
The delivery here is 'Delivery to HSE' and this is 
what you input in the xml-rpc script.
"en_GB" and "en_US" just mean it's in both languages in the GUI.
Example:
operation_name = "Delivery to HSE"

*/
SELECT id, name
FROM stock_picking_type;

/*
variable: location_id
The sql query will show the parent location
and location so you won't get mixed up as 
sometimes the child location could be the same
but with different parents.
Example:
location_id = 26
*/
SELECT 
    child.id AS location_id,
    child.name AS location_name,
    parent.name AS parent_location_name
FROM 
    stock_location child
LEFT JOIN 
    stock_location parent ON child.location_id = parent.id
WHERE 
    child.name ILIKE '%HSE%' OR child.name ILIKE '%WH%';
    
/*
variable: product_uom
The sql query uses 'en_US' so adjust
based on your language
Example:
product_uom = 1
*/
SELECT id, name->>'en_US' AS uom_name
FROM uom_uom
WHERE name->>'en_US' ILIKE '%Unit%';

/*
variable: product_uom_qty (variant)
You should always know your quantity before hand.
Example:
product_uom_qty = 10
This is simply the quantity to deliver
But just in case.  Product variants and their
quantities by location
*/
SELECT 
    pp.id AS product_id,
    pt.name->>'en_US' AS base_name,
    STRING_AGG(DISTINCT pav.name->>'en_US', ', ') AS attribute_values,
    CASE 
        WHEN COUNT(pav.name) > 0 
        THEN pt.name->>'en_US' || ' (' || STRING_AGG(DISTINCT pav.name->>'en_US', ', ') || ')'
        ELSE pt.name->>'en_US'
    END AS full_variant_name,
    sl.name AS location_name,
    SUM(sq.quantity) AS total_quantity
FROM 
    product_product pp
JOIN 
    product_template pt ON pp.product_tmpl_id = pt.id
JOIN 
    product_variant_combination pvc ON pvc.product_product_id = pp.id
JOIN 
    product_template_attribute_value ptav ON ptav.id = pvc.product_template_attribute_value_id
JOIN 
    product_attribute_value pav ON pav.id = ptav.product_attribute_value_id
LEFT JOIN 
    stock_quant sq ON sq.product_id = pp.id
LEFT JOIN 
    stock_location sl ON sl.id = sq.location_id
WHERE 
    pt.name->>'en_US' = 'Coffee Mug'
GROUP BY 
    pp.id, pt.name, sl.name
ORDER BY 
    full_variant_name, location_name;

/*
/*
variable: product_uom_qty (straight product)
You should always know your quantity before hand.
Example:
product_uom_qty = 10
This is simply the quantity to deliver
But just in case.  Product and their
quantities by location
*/
*/


