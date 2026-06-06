import os
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ec.settings")
django.setup()

from app.models import Product

print("Starting import...")

with open("data.json", "r", encoding="utf-16-sig") as f:
    data = json.load(f)

count = 0

for item in data:
    if item["model"] == "app.product":
        fields = item["fields"]

        Product.objects.create(
            title=fields["title"],
            selling_price=fields["selling_price"],
            discounted_price=fields["discounted_price"],
            description=fields["description"],
            category=fields["category"],
            product_image=fields["product_image"],
        )
        count += 1

print("Done importing:", count)