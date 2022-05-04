import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import urllib.request
from PIL import ImageTk, Image
import os


def retrieveHTML(URL):
    source = requests.get(URL, headers=hdr)
    soup = BeautifulSoup(source.text, 'html.parser')
    return soup


def parsePriceElementsOfHTML(soup):
    prices = soup.findAll(class_="pull-right price")
    finalPrices = []
    for i in range(5):
        finalPrices.append(prices[i].get_text())
    return finalPrices


def parseNameElementsOfHTML(soup):
    product_names = soup.findAll(class_="title")
    names = []
    for i in range(5):
        names.append(product_names[i].get_text())
    return names


def parseImagesElementsOfHTML(soup, baseURL):
    imageLinks = soup.findAll(class_="img-responsive")
    finalImages = []
    for i in range(5):
        imageLinks[i] = baseURL + imageLinks[i].attrs['src']
        finalImages.append(imageLinks[i])
        urllib.request.urlretrieve(imageLinks[i], "images/productImage" + str(i) + ".jpg")
    return finalImages


def parsePriceElementsOfHTMLNewegg(soup):
    prices = soup.findAll(['strong', 'sup'])
    finalPrices = []
    begin = False
    for i in range(len(prices)):
        if begin:
            finalPrices.append(prices[i].get_text() + prices[i + 1].get_text())
            return finalPrices
        if "Hide" in prices[i].get_text():
            begin = True
    return finalPrices


def parseNameElementsOfHTMLNewegg(soup):
    product_names = soup.findAll(class_="item-title")
    names = []
    for i in range(1):
        names.append(product_names[i].get_text())
    return names


def parseImagesElementsOfHTMLNewegg(soup, totalProductImages):
    imageLinks = soup.findAll("img")
    finalImages = []
    index = 2
    if len(imageLinks) == 10:
        index = 6
    finalImages.append(imageLinks[index].attrs['src'])
    urllib.request.urlretrieve(finalImages[0], "images/productImage" + str(totalProductImages) + ".png")
    return finalImages


def parseNameElementsOfHTMLWalmart(soup):
    product_names = soup.findAll(class_='f6 f5-l normal dark-gray mb0 mt1 lh-title')
    names = []
    if product_names is None or len(product_names) < 1:
        return
    else:
        for i in range(1):
            names.append(product_names[i].get_text())
    return names


def parsePriceElementsOfHTMLWalmart(soup):
    j = 0
    k = 1
    prices = soup.findAll(class_='b black f5 mr1 mr2-xl lh-copy f4-l')
    if prices is None or len(prices) < 1:
        return
    else:
        if len(prices) > 1:
            j = len(prices) - 2
            k = len(prices) - 1
        finalPrices = []
        for i in range(j, k):
            finalPrices.append(prices[i].get_text())
    return finalPrices


def parseImagesElementsOfHTMLWalmart(soup, totalProductImages):
    imageLinks = soup.findAll("img", {"loading": "eager"})
    finalImages = []
    if imageLinks is None or len(imageLinks) < 1:
        return
    else:
        finalImages.append(imageLinks[0].attrs['src'])
        urllib.request.urlretrieve(finalImages[0], "images/productImage" + str(totalProductImages) + ".png")
    return finalImages


def parseNameElementsOfHTMLBestBuy(soup):
    product_names = soup.find(class_="sku-header")
    names = []
    if product_names is None or len(product_names) < 1:
        return 0
    else:
        for i in range(1):
            names.append(product_names.get_text())
    return names


def parsePriceElementsOfHTMLBestBuy(soup):
    prices = soup.findAll("span", {"aria-hidden": "true"})
    finalPrices = []
    if prices is None or len(prices) < 1:
        return
    else:
        for i in range(2):
            if '$' in prices[i].get_text():
                finalPrices.append(prices[i].get_text())
    return finalPrices


def parseImagesElementsOfHTMLBestBuy(soup, totalProductImages):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    imageLinks = soup.findAll("img", class_="product-image")
    finalImages = []
    if imageLinks is None or len(imageLinks) < 1:
        return
    else:
        finalImages.append(imageLinks[0].attrs['src'])
        r = requests.get(imageLinks[0].attrs['src'], stream=True, headers=hdr)
        if r.status_code == 200:
            with open(dir_path + "/images/productImage" + str(totalProductImages) + ".png", 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
    return finalImages


def parseNameElementsOfHTMLBestBuy3(soup):
    product_names = soup.findAll(class_="sku-title")
    names = []
    if product_names is None or len(product_names) < 3:
        return
    else:
        for i in range(3):
            names.append(product_names[i].get_text())
    return names


def parsePriceElementsOfHTMLBestBuy3(soup):
    prices = soup.findAll("span", {"aria-hidden": "true"})
    finalPrices = []
    if prices is None or len(prices) < 3:
        return
    else:
        for i in range(6):
            if '$' in prices[i].get_text():
                finalPrices.append(prices[i].get_text())
    return finalPrices


def parseImagesElementsOfHTMLBestBuy3(soup):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    imageLinks = soup.findAll("img", class_="product-image")
    finalImages = []
    if imageLinks is None or len(imageLinks) < 3:
        return
    else:
        for i in range(3):
            finalImages.append(imageLinks[i].attrs['src'])
            r = requests.get(imageLinks[i].attrs['src'], stream=True, headers=hdr)
            if r.status_code == 200:
                with open(dir_path + "/images/productImage" + str(i) + ".png", 'wb') as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
    return finalImages


def topThreeResults():
    keywordSearch = productName_entry.get().replace(' ', '+')
    tempArray = 'https://www.bestbuy.com/site/searchpage.jsp?st=' + keywordSearch
    soup = retrieveHTML(tempArray)
    product_names = parseNameElementsOfHTMLBestBuy3(soup)
    imageLinks = parseImagesElementsOfHTMLBestBuy3(soup)
    product_prices = parsePriceElementsOfHTMLBestBuy3(soup)

    if product_names is None or imageLinks is None:
        tkinter.messagebox.showerror(title="Product Search Error", message="Unable to find product", )
    elif len(product_names) < 2 or len(imageLinks) < 2:
        tkinter.messagebox.showerror(title="Product Search Error", message="Unable to find product", )
    else:
        confirmWindow = tk.Toplevel()
        confirmWindow.title = "Confirm Search"
        confirmWindow.geometry('800x400')
        img0 = ImageTk.PhotoImage(Image.open("images/productImage" + str(0) + ".png"))
        gridImage0 = tk.Label(confirmWindow, image=img0)
        img1 = ImageTk.PhotoImage(Image.open("images/productImage" + str(1) + ".png"))
        gridImage1 = tk.Label(confirmWindow, image=img1)
        img2 = ImageTk.PhotoImage(Image.open("images/productImage" + str(2) + ".png"))
        gridImage2 = tk.Label(confirmWindow, image=img2)
        ProductNameOne_label = ttk.Label(confirmWindow, text="Name: " + product_names[0], wraplength=120)
        ProductNameTwo_label = ttk.Label(confirmWindow, text="Name: " + product_names[1], wraplength=120)
        ProductNameThree_label = ttk.Label(confirmWindow, text="Name: " + product_names[2], wraplength=120)

        confirm_button1 = ttk.Button(
            confirmWindow,
            text='Confirm',
            command=lambda: display_cheapest(product_names[0], product_names[0], product_prices[0], imageLinks[0],
                                             img0)
        )
        confirm_button2 = ttk.Button(
            confirmWindow,
            text='Confirm',
            command=lambda: display_cheapest(product_names[1], product_names[1], product_prices[1], imageLinks[1],
                                             img1)
        )
        confirm_button3 = ttk.Button(
            confirmWindow,
            text='Confirm',
            command=lambda: display_cheapest(product_names[2], product_names[2], product_prices[2], imageLinks[2],
                                             img2)
        )

        gridImage0.grid(row=0, column=0)
        gridImage1.grid(row=0, column=1)
        gridImage2.grid(row=0, column=2)
        ProductNameOne_label.grid(row=1, column=0)
        ProductNameTwo_label.grid(row=1, column=1)
        ProductNameThree_label.grid(row=1, column=2)
        confirm_button1.grid(row=2, column=0)
        confirm_button2.grid(row=2, column=1)
        confirm_button3.grid(row=2, column=2)

        confirmWindow.mainloop()


def display_cheapest( confirmedSearch, firstName, firstPrice, imageLink, firstImage):
    totalProductImages = 0
    retailers = []
    keywordSearch = confirmedSearch.replace(' ', '+')
    keywordSearch = keywordSearch.replace('-', '')

    product_names = []
    prices = []
    imageLinks = []

    if CheckVar3.get():
        tempArray = 'https://www.walmart.com/search?q=' + keywordSearch
        soup = retrieveHTML(tempArray)
        product_names = parseNameElementsOfHTMLWalmart(soup)
        prices = parsePriceElementsOfHTMLWalmart(soup)
        imageLinks = parseImagesElementsOfHTMLWalmart(soup, totalProductImages)
        retailers.append("Walmart")
        totalProductImages += 1

    if CheckVar2.get():
        product_names.append(firstName)
        prices.append(firstPrice)
        retailers.append("BestBuy")
        imageLinks.append(imageLink)
        totalProductImages += 1

    if CheckVar1.get():
        tempArray = 'https://www.newegg.com/p/pl?d=' + keywordSearch
        soup = retrieveHTML(tempArray)
        product_names += parseNameElementsOfHTMLNewegg(soup)
        prices += parsePriceElementsOfHTMLNewegg(soup)
        imageLinks += parseImagesElementsOfHTMLNewegg(soup, totalProductImages)
        retailers.append("Newegg")
        totalProductImages += 1

    if product_names is None or imageLinks is None or prices is None:
        tkinter.messagebox.showerror(title="Product Search Error", message="Unable to find product")
    elif len(product_names) < 1 or len(imageLinks) < 1 or len(prices) < 1 or len(retailers) < 1:
        tkinter.messagebox.showerror(title="Product Search Error", message="No Retailers selected")
    elif len(product_names) != len(imageLinks) or len(imageLinks) != len(prices) or len(prices) != len(product_names):
        tkinter.messagebox.showerror(title="Product Search Error", message="Unable to find product")
    else:
        try:
            df = pd.DataFrame({
                "names": product_names,
                "prices": prices,
                "images": imageLinks,
                "retailer": retailers
            })
        except:
            tkinter.messagebox.showerror(title="Product Search Error",
                                         message="Unable to find product" + str(len(product_names)) + str(
                                             len(prices)) + str(len(retailers)))
            return

        numPrices = []
        for numeric_string in prices:
            if "$" in numeric_string:
                numeric_string = numeric_string.replace("$", "")
                numeric_string = numeric_string.replace(",", "")
            numPrices.append(float(numeric_string))
        indexOfCheapestPrice = numPrices.index(min(numPrices))
        df.to_csv(r'export_dataframe.csv')

        results = tk.Toplevel()
        results.title = "Results"
        canvas = tk.Canvas(results, width=400, height=400)
        canvas.pack()
        if retailers[indexOfCheapestPrice] == "BestBuy":
            img = firstImage
        else:
            img = ImageTk.PhotoImage(Image.open("images/productImage" + str(indexOfCheapestPrice) + ".png"))
        canvas.create_image(150, 150, image=img)
        cheapestProductName_label = ttk.Label(results, text="Name: " + product_names[indexOfCheapestPrice])
        cheapestProductName_label.place(relx=0.0,
                                        rely=0.85,
                                        anchor='sw')
        cheapestPrice_label = ttk.Label(results, text="Price: " + prices[indexOfCheapestPrice])
        cheapestPrice_label.place(relx=0.0,
                                  rely=0.9,
                                  anchor='sw')
        retailerName_label = ttk.Label(results, text="Retailer: " + retailers[indexOfCheapestPrice])
        retailerName_label.place(relx=0.0,
                                 rely=0.95,
                                 anchor='sw')
        results.mainloop()


window = tk.Tk()
window.title("Best Price Search Tool")
window_width = 600
window_height = 400
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)
window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
window.resizable(False, False)
frame = ttk.Frame(window)
frame.pack(padx=10, pady=10, fill='x', expand=True)

ua = UserAgent()
hdr = {
    "User-Agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
CheckVar1 = tk.IntVar()
CheckVar2 = tk.IntVar()
CheckVar3 = tk.IntVar()
C1 = tk.Checkbutton(window, text="Newegg", variable=CheckVar1,
                    onvalue=1, offvalue=0, height=5,
                    width=10)
C2 = tk.Checkbutton(window, text="BestBuy", variable=CheckVar2,
                    onvalue=1, offvalue=0, height=5,
                    width=10)
C3 = tk.Checkbutton(window, text="Walmart", variable=CheckVar3,
                    onvalue=1, offvalue=0, height=5,
                    width=10)
C1.pack(side="right")
C2.pack(side="right")
C3.pack(side="right")

productName = tk.StringVar()
productName_label = ttk.Label(frame, text="Product Name:")
productName_label.pack(fill='x', expand=True)
productName_entry = ttk.Entry(frame, textvariable=productName)
productName_entry.pack(fill='x', expand=True)
productName_entry.focus()

blank_label = ttk.Label(frame, text="")
blank_label.pack(fill='x', expand=True)

search_button = ttk.Button(
    frame,
    text='Search',
    command=lambda: topThreeResults()
)
search_button.pack(
    ipadx=5,
    ipady=5,
    side="left"
)

exit_button = ttk.Button(
    frame,
    text='Exit',
    command=lambda: window.quit()
)
exit_button.pack(
    ipadx=5,
    ipady=5,
    side="right"
)

window.mainloop()
