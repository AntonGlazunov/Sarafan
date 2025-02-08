import os


def upload_to_product(instance, filename):
    base_name = os.path.basename(filename)
    name, ext = os.path.splitext(base_name)
    new_name = f"{instance.slug}{ext}"
    return os.path.join('shop', 'product', new_name)

def upload_to_category(instance, filename):
    base_name = os.path.basename(filename)
    name, ext = os.path.splitext(base_name)
    new_name = f"{instance.slug}{ext}"
    return os.path.join('shop', 'category', new_name)

def upload_to_subcategory(instance, filename):
    base_name = os.path.basename(filename)
    name, ext = os.path.splitext(base_name)
    new_name = f"{instance.slug}{ext}"
    return os.path.join('shop', 'subcategory', new_name)
