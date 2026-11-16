FILE = "products.txt"
products = []   # list of dictionaries
cart = {}       # {product_id: quantity}


def num(s):
    n = float(s)
    return int(n) if n.is_integer() else n


def load():
    try:
        with open(FILE) as f:
            for line in f:
                if line.strip():
                    i, n, p, s = line.strip().split(",")
                    products.append({"id": i, "name": n, "price": num(p), "stock": int(s)})
    except FileNotFoundError:
        pass


def save():
    with open(FILE, "w") as f:
        for p in products:
            f.write(f"{p['id']},{p['name']},{p['price']},{p['stock']}\n")


def find(pid):
    for p in products:
        if p["id"] == pid:
            return p


def show(p):
    print(f"ID: {p['id']} | {p['name']} | Price: {p['price']} | Stock: {p['stock']}")


def read_price_stock():
    try:
        price = num(input("Price: "))
    except ValueError:
        price = 0
    if price <= 0:
        print("Invalid price. Price must be a positive number.")
        return None
    try:
        stock = int(input("Stock: "))
        if stock < 0:
            raise ValueError
    except ValueError:
        print("Invalid stock. Stock must be 0 or more.")
        return None
    return price, stock

#! option 1
def add_product():
    name = input("Name: ")
    data = read_price_stock()
    if not data:
        return
    pid = "P" + str(max([int(p["id"][1:]) for p in products], default=100) + 1)
    p = {"id": pid, "name": name, "price": data[0], "stock": data[1]}
    products.append(p)
    save()
    print("Product added.", end=" " if p["stock"] == 0 else "\n")
    show(p)
    if p["stock"] == 0:
        print(f"Warning: {name} is out of stock.")

#! option 2
def update_product():
    pid = input("Product ID: ")
    p = find(pid)
    if not p:
        return print(f"Product {pid} not found.")
    data = read_price_stock()
    if not data:
        return
    p["price"], p["stock"] = data
    cart.pop(pid, None)  # cart quantity may no longer match the new stock
    save()
    print("Product updated.")
    show(p)

#! option 3
def delete_product():
    pid = input("Product ID: ")
    p = find(pid)
    if not p:
        return print(f"Product {pid} not found.")
    products.remove(p)
    cart.pop(pid, None)
    save()
    print(f"Product '{p['name']}' deleted. Products left: {len(products)}")

#! option 4
def view_products():
    if not products:
        print("No products.")
    for p in products:
        show(p)

#! option 5
def add_to_cart():
    pid = input("Product ID: ")
    p = find(pid)
    if not p:
        return print(f"Product {pid} not found.")
    try:
        qty = int(input("Quantity: "))
    except ValueError:
        qty = 0
    if qty <= 0:
        return print("Invalid quantity.")
    if cart.get(pid, 0) + qty > p["stock"]:
        return print(f"Not enough stock. Available: {p['stock']}")
    cart[pid] = cart.get(pid, 0) + qty
    print(f"{p['name']} x{qty} added | Amount: {p['price'] * qty}")

#! option 6 
def checkout():
    if not cart:
        return print("Cart is empty.")
    total, left = 0, []
    for pid, qty in cart.items():
        p = find(pid)
        p["stock"] -= qty
        total += p["price"] * qty
        left.append(f"{p['name']} stock left: {p['stock']}")
    cart.clear()
    save()
    print(f"Order total: {total} | " + " | ".join(left))


load()
menu = {"1": add_product, "2": update_product, "3": delete_product,
        "4": view_products, "5": add_to_cart, "6": checkout}
while True:
    print("\n1.Add  2.Update  3.Delete  4.View  5.Add to cart  6.Checkout  7.Exit")
    c = input("Choose: ")
    if c == "7":
        break
    menu.get(c, lambda: print("Invalid option."))()