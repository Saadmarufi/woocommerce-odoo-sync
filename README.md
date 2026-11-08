# woocommerce-odoo-sync

Lightweight Python utility for formatting and synchronizing e-commerce product catalog and stock data between WooCommerce and Odoo ERP.

## Synchronization Workflow
1. **Fetch & Extract**: Ingest raw product JSON payloads from the WooCommerce REST API (`/wp-json/wc/v3/products`).
2. **Normalize Data**: Clean, format, and map fields into a consistent schema (e.g. converting string numbers to floats/ints, standardizing SKUs).
3. **Payload Batching**: Partition normalized records into optimal batch payloads for transmission to Odoo XML-RPC / JSON-RPC endpoints.
4. **Push & Sync**: Upsert inventory stock levels and pricing records into Odoo (`product.product` / `product.template`).

## Field Mapping
| Field | WooCommerce Source | Odoo Destination | Notes |
| :--- | :--- | :--- | :--- |
| **SKU** | `sku` | `default_code` | Product unique identifier / internal reference |
| **Stock Quantity** | `stock_quantity` | `qty_available` | Real-time available physical stock level |
| **Pricing** | `regular_price` / `price` | `list_price` | Standard selling price |

## Usage
Run the synchronization script directly via Python:
```bash
python sync_catalog.py
```
