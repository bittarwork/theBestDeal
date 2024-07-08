import requests
from bs4 import BeautifulSoup
import csv


def get_amazon_deals(product_name):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    url = f"https://www.amazon.sa/s?k={product_name.replace(' ', '+')}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return "Error: Unable to fetch data from Amazon"

    soup = BeautifulSoup(response.content, "html.parser")
    deals = []

    divs = soup.find_all('div', {'class': 'sg-col-inner'})
    for div in divs:
        name = div.find(
            'span', {'class': 'a-size-base-plus a-color-base a-text-normal'})
        itemPrice = div.find('span', {'class': 'a-price-whole'})
        itemLink = div.find(
            "a", {"class": "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})

        if name and itemPrice and itemLink:
            deals.append({
                "title": name.text.strip(),
                "price": itemPrice.text.strip().replace(",", ""),
                "link": f"https://www.amazon.sa{itemLink['href']}"
            })

    return deals


def save_deals_to_file(deals, filename):
    keys = deals[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(deals)


def main():
    while True:
        print("Enter 'exit' to quit the program.")

        product_name = input("Please enter the product name: ")
        if product_name.lower() == 'exit':
            break

        print(f"Searching for {product_name} in Amazon.sa...")

        amazon_deals = get_amazon_deals(product_name)
        if isinstance(amazon_deals, str):
            print(amazon_deals)
            continue

        if not amazon_deals:
            print("No deals found.")
            continue

        filename = f"{product_name.replace(' ', '_')}_deals.csv"
        save_deals_to_file(amazon_deals, filename)
        print(f"Deals saved to {filename}\n")


if __name__ == "__main__":
    main()
