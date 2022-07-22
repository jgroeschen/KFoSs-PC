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
- [ ] Creating reports of the best current sales 
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


# Running the program

This project was developed under Python 3, most recently with version 3.10.4.

## How to Run the Program
The 

1. Download this repo (KFoSs-PC) or clone `https://github.com/jgroeschen/KFoSs-PC.git` to your computer and navigate to the folder containing this project's code

2. Recommended (but not required): create a [virtual environment](https://docs.python.org/3/tutorial/venv.html) to run the program without affecting any packages you have installed currently

3. Use `pip` to install the required versions of the modules imported by this program

    Usually: `pip install -r requirements.txt` or `pip3 install -r requirements.txt`

    Otherwise you can try:

    On Windows: `py -m pip install -r requirements.txt`

    On Unix or macOS: `python -m pip install -r requirements.txt`

4. Run `gui.py`

        python gui.py
    and the gui will load. 

5. If this is the first time you have run the program, you will have to enter credentials obtained from the [Kroger Developer site](developer.kroger.com).
Register, create an app under the "Production" environment, and use the credentials you create. 
The credentials I am using to test this application are not provided in the Github repo, for security purposes.
**Code Louisville/Code Kentucky mentor(s) reviewing this project have access to the credentials provided via the project submission form.**

6. Once your credentials are verified, you can select the (presumably local) store you'd like to use as a data source for pricing information.
Select the name of the chain, enter your ZIP code, find nearby stores, choose your store from the dropdown, and click the select button.

7. You will be transferred to the "Price Checker" tab, where you can enter a search term and hit Enter or cick the "Search" button to populate the left frame with results.
    > **_NOTE:_**  This will hang the program for approximately five seconds (at least on my ~decade-old desktop), as currently it writes compressed data to "pricing-data.csv.xz" and is not yet threaded (and may not be for some time). Compressing to ".xz" results in a csv that is about 10% of the uncompressed size, so I decided the tradeoff was worth it. Extracting the uncompressed csv (I use [7-zip](https://www.7-zip.org/)) to the project directory alongside the compressed file and replacing the (currently two) instances of ".csv.xz" with ".csv" (both without the double quote marks) in gui.py will change this behavior. In the time it took me to write this note, I might have been able to add a setting in gui.py to switch, but I'm already invested here, I guess.

8. Clicking any of the results populates the right frame with information about your selection, including a graph of historical prices.
    > **_NOTE:_**  The "pricing-data.csv.xz" file included in this repo contains pricing data that has been pseudo-randomly anonymized for all dates prior to 2022-07-21, and should not be taken to be authoritative.


### **Credits and Acknowledgements**

The code contained in this project is the product of my own mind


### **Legal**

All brand names, trademarks, registered trademarks, and product names are the property of their respective owners.
The names of any businesses, goods, or services mentioned here are used solely for the purpose of identification.
No relationship or endorsement is expressed or implied by the presence of these marks.