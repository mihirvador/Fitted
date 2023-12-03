import requests

url = "https://fitted-api-9e3i.onrender.com/"

data = {"title": "BUREAU PANT", 
        "url": "https://www.aritzia.com/us/en/product/bureau-pant/111799033.html",
          "image": "https://aritzia.scene7.com/is/image/Aritzia/large/f23_01_a06_111799_2569_on_a.jpg"
        , "site_name": "Aritzia.com", "price:amount": "168.00"}
out = requests.post(url+"/input", data=data)
print(out.json())