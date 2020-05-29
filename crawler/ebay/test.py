import copy


def math_range():
    for i in range(0, 10):
        print(i)


if __name__ == '__main__':
    math_range()
    dict = {"product_name": "AAA", "product_price": "35.5元",
            "product_url": "https://www.ebay.com/itm/Christmas-Gift-Walking-Dragon-Toy-Fire-Breathing-Water-Spray-Dinosaur-Toy/264637455878?hash=item3d9d9f1e06:m:mnVqj7Pta4Jc7OexVstYO8A&var=564430296399",
            "product_image": "https://i.ebayimg.com/thumbs/images/m/mnVqj7Pta4Jc7OexVstYO8A/s-l225.jpg"}
    dict1=copy.deepcopy(dict)
    dict1["product_price"]="26元"
    print(dict)
    print(dict1)