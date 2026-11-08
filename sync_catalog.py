"""
WooCommerce to Odoo Catalog & Stock Sync Utility

Normalizes product/SKU records and prepares payload batches for synchronization
between WooCommerce REST API and Odoo ERP XML-RPC / JSON-RPC endpoints.
"""

from typing import List, Dict, Any


class ProductSyncPipeline:
    def __init__(self, batch_size: int = 50):
        self.batch_size = batch_size

    def normalize_wc_product(self, wc_product: Dict[str, Any]) -> Dict[str, Any]:
        """Normalizes a raw WooCommerce product record into a unified catalog item."""
        return {
            "sku": str(wc_product.get("sku", "")).strip().upper(),
            "name": str(wc_product.get("name", "")).strip(),
            "price": float(wc_product.get("regular_price", 0.0) or 0.0),
            "stock_quantity": int(wc_product.get("stock_quantity", 0) or 0),
            "status": "active" if wc_product.get("status") == "publish" else "draft",
        }

    def prepare_odoo_payload(self, normalized_products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Formats normalized products into Odoo product.product model record payloads."""
        payloads = []
        for item in normalized_products:
            payloads.append({
                "default_code": item["sku"],  # Odoo internal reference (SKU)
                "name": item["name"],
                "list_price": item["price"],
                "qty_available": item["stock_quantity"],
            })
        return payloads

    def create_batches(self, records: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
        """Splits list of records into payload batches for API request execution."""
        return [records[i : i + self.batch_size] for i in range(0, len(records), self.batch_size)]


if __name__ == "__main__":
    sample_wc_data = [
        {"sku": "PB-TSHIRT-01", "name": "Pixel & Brush Branded Tee", "regular_price": "29.99", "stock_quantity": 100, "status": "publish"},
        {"sku": "PB-POSTER-02", "name": "Vector Art Print A2", "regular_price": "14.50", "stock_quantity": 45, "status": "publish"},
    ]

    pipeline = ProductSyncPipeline(batch_size=10)
    normalized = [pipeline.normalize_wc_product(item) for item in sample_wc_data]
    odoo_payloads = pipeline.prepare_odoo_payload(normalized)
    batches = pipeline.create_batches(odoo_payloads)

    print(f"Normalized {len(normalized)} records into {len(batches)} batch(es).")
    print("Sample Odoo Payload Batch:", batches[0])
