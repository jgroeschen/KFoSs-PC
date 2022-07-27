# **The Home of the KFoSs-PC Project**

Thusly named because it is a 
***K***roger ***F***amily ***o***f ***S***tore***s*** ***P***rice ***C***hecker
and also because it connects you to ***K***roger's API via 
***f***ree, ***o***pen-***s***ource ***s***oftware for your ***p***ersonal ***c***omputer 


This project is in the early stages of development.
It is, at present, a final project for the Code Kentucky/Code Louisville Data Analysis 1 course, but I plan to continue to develop it after the conclusion of the class.


Current features planned include:
- [x] Oauth2 credential authentication
- [x] Finding local stores with the Locations API
- [x] Checking prices on-demand with the Products API
- [x] Tracking regular and sale prices over time
- [x] Creating reports of the best current sales 
- [x] Unit price comparisons


Eventual planned features:
- [ ] Historical low price reports
- [ ] Local search to reduce API calls
- [ ] Local sub-lists
- [ ] Scheduled refreshing


Dream goals:
- [ ] Cross-checking against coupons with the Identity/Cart API
- [ ] Rebates, too
- [ ] Searching multiple stores concurrently

# Code Kentucky/Code Louisville Requirements

1. I used the `requests` library to read data in from Kroger's [public API](https://api.kroger.com/), using both the "Products" and "Locations" APIs.

2. The data is returned from the API in JSON format, and is generally pretty clean and organized, but some was missing or wrong and some was extraneous. For example, if an item is not on sale, the "promo" key has a value of zero rather than being blank or null. The "Locations" API, on the other hand, returns chain names that aren't Kroger subsidiaries and locations of warehouses mixed in with publicly-accessible stores.

3. The "Products" API doesn't return some information that I wanted to see. In addition to not showing past pricing data, it also doesn't provide unit prices or information about the percentage by which a product is discounted. With the help of the `pint` library, I wrote code to parse and display unit prices standardized for both liquid and solid measures. Some units returned by the API were unusable (especially ones including both count and size, which were inconsistent on whether the size was total or individual), and were excluded. Percentage discounts were a simpler subtraction of the promo price divided by the regular price from one, then standardized into a percentage.

4. A themed and customized version of `tkinter`, `customtkinter`, provided a GUI framework to display, among other things, plots of both regular prices and promotional prices whenever a user searched for a product, including historical prices for thousands of items.

# Running the program

This project was developed under Python 3, most recently with version 3.10.4. Its layout was designed on a desktop with a display resolution of 1920x1080; other resolutions may not show the GUI properly. It runs as expected on Windows 10 (10.0.17763) and Ubuntu 20.04.2 LTS, but I have not tested it on MacOS or other systems not listed.


## How to Run the Program

1. Download this repo (KFoSs-PC) or clone `https://github.com/jgroeschen/KFoSs-PC.git` to your computer and navigate to the folder containing this project's code.

        git clone https://github.com/jgroeschen/KFoSs-PC.git

        cd KFoSs-PC

2. Recommended (but not required): create and activate a [virtual environment](https://docs.python.org/3/tutorial/venv.html) to run the program without affecting any packages you have installed currently.

3. Use `pip` to install the required versions of the modules imported by this program.

    Usually: `pip install -r requirements.txt` or `pip3 install -r requirements.txt`

    Otherwise you can try:

    On Windows: `py -m pip install -r requirements.txt`

    On Unix or macOS: `python -m pip install -r requirements.txt`

4. Run `gui.py`

        python gui.py
    and the gui will load. 

5. If this is the first time you have run the program, you will have to enter credentials obtained from the [Kroger Developer site](https://developer.kroger.com).
Register, create an app under the "Production" environment, and use the credentials you create. 
The credentials I am using to test this application are not provided in the Github repo, for security purposes.

    > **Code Louisville/Code Kentucky mentor(s) reviewing this project have access to the credentials provided via the project submission form.**

6. Once your credentials are verified, you can select the (presumably local) store you'd like to use as a data source for pricing information.
Select the name of the chain, enter your ZIP code, find nearby stores, choose your store from the dropdown, and click the select button.

7. You will be transferred to the "Price Checker" tab, where you can enter a search term and hit Enter or click the "Search" button to populate the left frame with results.
    > **_NOTE:_**  This will hang the program for approximately five seconds (at least on my ~decade-old desktop), as currently it writes compressed data to "pricing-data.csv.xz" and is not yet threaded (and may not be for some time). Compressing to ".xz" results in a csv that is about 10% of the uncompressed size, so I decided the tradeoff was worth it.

8. Clicking any of the results populates the right frame with information about your selection, including a graph of historical prices.
    > **_NOTE:_**  The "pricing-data.csv.xz" file included in this repo contains pricing data that has been pseudo-randomly anonymized for all dates prior to 2022-07-21, and should not be taken to be authoritative.

9. The "Historical Prices" tab contains a `pandastable` visualization of the DataFrame in the form of a spreadsheet of the data, with pricing shown by date in a regular|promo format.

10. The "Best Sales" tab contains a button to activate/refresh another `pandastable` visualization, this time of all the most recent items with promotional prices, sorted in descending order by the percentage the product has been discounted from its regular price.


### **Credits and Acknowledgments**

The code contained in this project is the product of my own mind.

Thanks to [TomSchimansky](https://github.com/TomSchimansky) for the work done on `customtkinter` to update the look of Python's standard GUI library, as well as all the others who have worked on the libraries used in this project.

Thanks to my wife for her unending support and love, throughout this project and always.

This project is dedicated in loving memory of Jerry, who always gave me a good-natured ribbing when I bought something from a Kroger competitor.




### **Legal**

All brand names, trademarks, registered trademarks, and product names are the property of their respective owners.
The names of any businesses, goods, or services mentioned here are used solely for the purpose of identification.
No relationship or endorsement is expressed or implied by the presence of these marks.