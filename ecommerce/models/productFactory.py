from ecommerce.models.product import \
    Shoe


class ProductFactory:
    def __init__(self):
        self.product_class = None

    TYPES = {
        "shoe": Shoe,
    }

    def set_product_class(self, category):
        self.product_class = self.TYPES.get(category.name)

    def create_product(self, **kwargs):
        if self.product_class is None:
            raise ValueError("Product class not set")
        return self.product_class(**kwargs)
