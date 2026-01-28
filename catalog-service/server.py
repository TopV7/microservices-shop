
with open("products.txt", "r", encoding="utf-8") as file:
    print("--- Catalog Service Products ---")
    for line in file:
        print(line.strip())

