import random

class TechnologyCompanyAPI:
    LAPTOP_NAMES = ["Dell XPS", "MacBook Pro", "HP Spectre x360", "Lenovo ThinkPad", "Asus ZenBook", "Microsoft Surface"]
    SMARTPHONE_NAMES = ["iPhone", "Samsung Galaxy", "Google Pixel", "OnePlus", "Huawei P", "Xiaomi Mi"]
    TABLET_NAMES = ["iPad", "Samsung Galaxy Tab", "Microsoft Surface Pro", "Amazon Fire", "Lenovo Tab", "Huawei MatePad"]
    WEARABLE_NAMES = ["Apple Watch", "Samsung Galaxy Watch", "Fitbit", "Garmin", "Xiaomi Mi Band", "Huawei Watch"]

    @staticmethod
    def get_products(num_products):
        """
        Generates mock JSON data representing products.
        Returns:
            list: A list of dictionaries representing products.
        """
        products = []
        for i in range(num_products):
            category = random.choice(["laptop", "smartphone", "tablet", "wearable"])
            if category == "laptop":
                name = random.choice(TechnologyCompanyAPI.LAPTOP_NAMES)
            elif category == "smartphone":
                name = random.choice(TechnologyCompanyAPI.SMARTPHONE_NAMES)
            elif category == "tablet":
                name = random.choice(TechnologyCompanyAPI.TABLET_NAMES)
            else:  # wearable
                name = random.choice(TechnologyCompanyAPI.WEARABLE_NAMES)

            product = {
                "id": i+1,
                "name": name,
                "price": random.randint(100, 2000),
                "category": category
            }
            products.append(product)
        return products
