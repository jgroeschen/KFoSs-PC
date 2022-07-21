import configparser
import time
import tkinter
import tkinter.messagebox
from tkinter import END

import customtkinter
from PIL import Image, ImageTk
from io import BytesIO
from oauthlib.oauth2 import BackendApplicationClient
import requests
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session
import pint
from datetime import datetime
import pandas as pd
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("System")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # define variables for token/exp, client id/secret, and store locations
        self.just_token = ''
        self.token_exp = ''
        self.client_id = ''
        self.client_secret = ''
        self.store_name = ''
        self.store_number = ''
        self.zip = ''

        # define ureg for pint
        self.ureg = pint.UnitRegistry()
        self.ureg.default_system = 'US'

        # Configure the window
        self.title("KFoSs-PC -- The Kroger Family of Stores Price Checker")
        self.iconbitmap('price_check_dark.ico')

        self.minsize(960, 540)
        self.geometry(
            f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        self.state('zoomed')

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Create a grid to hold left and right side frames ===================
        self.grid_columnconfigure(0, weight=0, minsize=200)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create the frames
        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 corner_radius=5)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_prices = customtkinter.CTkFrame(master=self)
        self.frame_prices.grid(row=0, column=1, sticky="nswe",
                               padx=10, pady=10)

        self.frame_historical_prices = customtkinter.CTkFrame(master=self)
        self.frame_historical_prices.grid(row=0, column=1, sticky="nswe",
                                          padx=10, pady=10)

        self.frame_closeouts = customtkinter.CTkFrame(master=self)
        self.frame_closeouts.grid(row=0, column=1, sticky="nswe",
                                  padx=10, pady=10)

        self.frame_settings = customtkinter.CTkFrame(master=self)
        self.frame_settings.grid(row=0, column=1, sticky="nswe",
                                 padx=10, pady=10)

        # Create and arrange frame_left
        self.frame_left.grid_rowconfigure(0, minsize=10)
        self.frame_left.grid_rowconfigure(2, minsize=10)
        self.frame_left.grid_rowconfigure(18, weight=1)
        self.frame_left.grid_rowconfigure(19, minsize=20)
        self.frame_left.grid_rowconfigure(21, minsize=10)

        self.left_title = customtkinter.CTkLabel(
            master=self.frame_left, text="KFoSs-PC",
            text_font=("Roboto Medium", -24))
        self.left_title.grid(row=1, pady=10, padx=10)

        self.price_check_button = customtkinter.CTkButton(
            master=self.frame_left, text="Price Checker",
            text_font=("Roboto", -18), fg_color=("gray70", "gray30"),
            command=self.prices_button_event)
        self.price_check_button.grid(row=3, pady=10, padx=10, ipadx=10,
                                     ipady=5, sticky="we")
        self.price_check_button.configure(state=tkinter.DISABLED)

        self.historical_prices_button = customtkinter.CTkButton(
            master=self.frame_left, text="Historical Prices",
            text_font=("Roboto", -18), fg_color=("gray70", "gray30"),
            command=self.historical_button_event)
        self.historical_prices_button.grid(row=4, pady=10, padx=10, ipadx=10,
                                           ipady=5, sticky="we")
        self.historical_prices_button.configure(state=tkinter.DISABLED)

        self.settings_button = customtkinter.CTkButton(
            master=self.frame_left, text="Settings",
            text_font=("Roboto", -18), fg_color=("gray70", "gray30"),
            command=self.settings_button_event)
        self.settings_button.grid(row=5, pady=10, padx=10, ipadx=10, ipady=5,
                                  sticky="we")

        self.dark_mode_switch = customtkinter.CTkSwitch(
            master=self.frame_left, text="Dark Mode",
            command=self.change_mode)
        self.dark_mode_switch.grid(row=20, pady=10, padx=20, sticky="w")
        self.dark_mode_switch.select()

        # Create and arrange frame_prices
        self.frame_prices.rowconfigure(0, weight=0)
        self.frame_prices.rowconfigure(1, weight=10)
        self.frame_prices.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7),
                                          weight=1, uniform='x')
        # self.frame_prices.columnconfigure(2, weight=0)

        self.product_search_bar = customtkinter.CTkEntry(
            master=self.frame_prices, )
        self.product_search_bar.grid(row=0, column=0, columnspan=5,
                                     sticky="nswe", padx=10, pady=10)
        self.product_search_bar.bind('<Return>',
                                     self.product_search_button_event)

        self.product_search_location = customtkinter.CTkOptionMenu(
            master=self.frame_prices, width=400,)
        self.product_search_location.grid(row=0, column=5, columnspan=2,
                                          sticky="nswe", padx=10, pady=10)

        self.product_search_button = customtkinter.CTkButton(
            master=self.frame_prices, text="Search",
            command=self.product_search_button_event)
        self.product_search_button.grid(row=0, column=7, sticky="nswe",
                                        padx=10, pady=10)

        self.subframe_product_list = customtkinter.CTkFrame(
            master=self.frame_prices)
        self.subframe_product_list.grid(row=1, column=0, columnspan=4,
                                        sticky="nswe", padx=10, pady=10)
        self.subframe_product_list.columnconfigure((0, 1,),
                                                   weight=1, uniform='x')

        self.subframe_product_info = customtkinter.CTkFrame(
            master=self.frame_prices)
        self.subframe_product_info.grid(row=1, column=4, columnspan=4,
                                        pady=10, padx=10, sticky="nsew")
        self.subframe_product_info.grid_columnconfigure(0, weight=1)
        self.subframe_product_info.grid_columnconfigure(1, weight=10)

        # Create and arrange frame_historical_prices

        # Create and arrange frame_closeouts

        # Create and arrange frame_settings
        self.frame_settings.grid_rowconfigure(0, minsize=10)
        self.frame_settings.grid_rowconfigure(2, minsize=10)
        self.frame_settings.grid_rowconfigure(4, minsize=10)

        self.settings_title = customtkinter.CTkLabel(
            master=self.frame_settings, text="KFoSs-PC Settings",
            text_font=("Roboto Medium", -24))
        self.settings_title.grid(row=1, column=0, pady=10, padx=10)

        # Create and arrange settings_subframe_credentials
        self.settings_subframe_credentials = customtkinter.CTkFrame(
            master=self.frame_settings)
        self.settings_subframe_credentials.grid(row=3, column=0, sticky="nswe",
                                                padx=20, pady=10)

        self.credentials_title = customtkinter.CTkLabel(
            master=self.settings_subframe_credentials, text="Credentials",
            text_font=("Roboto Medium", -24))
        self.credentials_title.grid(row=0, column=0, columnspan=3,
                                    sticky="nswe", padx=20, pady=20)

        self.credentials_id_label = customtkinter.CTkLabel(
            master=self.settings_subframe_credentials, text="Enter your ID:")
        self.credentials_id_label.grid(row=1, column=0, sticky="w",
                                       padx=20, pady=20)

        self.credentials_id_entry = customtkinter.CTkEntry(
            master=self.settings_subframe_credentials)
        self.credentials_id_entry.grid(row=1, column=1, sticky="w",
                                       padx=20, pady=20)

        self.credentials_secret_label = customtkinter.CTkLabel(
            master=self.settings_subframe_credentials,
            text="Enter your Secret:")
        self.credentials_secret_label.grid(row=3, column=0, sticky="w",
                                           padx=20, pady=20)

        self.credentials_secret_entry = customtkinter.CTkEntry(
            master=self.settings_subframe_credentials, show="*")
        self.credentials_secret_entry.grid(row=3, column=1, sticky="w",
                                           padx=20, pady=20)

        self.credentials_button = customtkinter.CTkButton(
            master=self.settings_subframe_credentials,
            text="Check your credentials",
            command=self.credentials_button_event)
        self.credentials_button.grid(row=1, column=3, rowspan=3, sticky="nswe",
                                     padx=20, pady=20)

        # Create and arrange settings_subframe_stores
        self.settings_subframe_stores = customtkinter.CTkFrame(
            master=self.frame_settings)
        self.settings_subframe_stores.grid(row=5, column=0, sticky="nswe",
                                           padx=20, pady=10)

        self.stores_title = customtkinter.CTkLabel(
            master=self.settings_subframe_stores, text="My Store",
            text_font=("Roboto Medium", -24))
        self.stores_title.grid(row=0, column=0, columnspan=3, sticky="nswe",
                               padx=20, pady=20)

        self.zip_label = customtkinter.CTkLabel(
            master=self.settings_subframe_stores, text="Enter your ZIP:").grid(
                row=2, column=0, sticky="w", padx=20, pady=20)

        self.zip_entry = customtkinter.CTkEntry(
            master=self.settings_subframe_stores)
        self.zip_entry.grid(row=2, column=1, sticky="nswe", padx=20, pady=20)

        self.chains_label = customtkinter.CTkLabel(
            master=self.settings_subframe_stores, text="Select chain:").grid(
                row=1, column=0, sticky="w", padx=20, pady=20)

        self.chains_optionmenu = customtkinter.CTkOptionMenu(
            master=self.settings_subframe_stores, values=[''])
        self.chains_optionmenu.grid(row=1, column=1, sticky="nswe",
                                    padx=20, pady=20)

        self.stores_optionmenu = customtkinter.CTkOptionMenu(
            master=self.settings_subframe_stores, values=[''], width=400)
        self.stores_optionmenu.grid(row=3, column=0, columnspan=2,
                                    sticky="nswe", padx=20, pady=20)

        self.stores_search_button = customtkinter.CTkButton(
            master=self.settings_subframe_stores, text="Find nearby stores",
            command=self.stores_search_button_event)
        self.stores_search_button.grid(row=2, column=3, rowspan=1,
                                       sticky="nswe", padx=20, pady=20)

        self.stores_select_button = customtkinter.CTkButton(
            master=self.settings_subframe_stores, text="Select this store",
            command=self.stores_select_button_event)
        self.stores_select_button.grid(row=3, column=3, rowspan=1,
                                       sticky="nswe", padx=20, pady=20)
        self.stores_select_button.configure(state="disabled")

        # Load Settings
        self.protocol('WM_TAKE_FOCUS', self.load_settings())

    # Token functions
    def get_token(self):
        # Oauthlib client id, secret, and scope
        auth = HTTPBasicAuth(self.client_id, self.client_secret)
        client = BackendApplicationClient(client_id=self.client_id,
                                          scope='product.compact')
        oauth = OAuth2Session(client=client, scope='product.compact')
        full_token = oauth.fetch_token(
            token_url='https://api.kroger.com/v1/connect/oauth2/token',
            auth=auth)
        self.just_token = full_token.get("access_token")
        self.token_exp = full_token.get("expires_at")
        self.write_config('token', 'just_token', str(self.just_token))
        self.write_config('token', 'token_exp', str(self.token_exp))

    def is_token_expiring(self):
        if (float(self.token_exp) - time.time()) < 300:
            self.get_token()
        else:
            pass

    # API functions
    def get_chains(self):
        heads = {
            "Accept": "application/json\\",
            "Authorization": "Bearer " + self.just_token,
        }
        self.is_token_expiring()
        chains_data = requests.get("https://api.kroger.com/v1/chains",
                                   headers=heads).json()
        chains_list = []
        for i in range(len(chains_data.get("data"))):
            chains_list.append(chains_data.get("data")[i].get("name"))
        chains_list = [e for e in chains_list if e not in (
            'AMOCO', 'BP', 'COPPS', 'COVID', 'EG GROUP', 'FRED',
            'FRESH EATS MKT', 'HARRIS TEETER FUEL',
            'HARRIS TEETER FUEL CENTER', 'HART', 'JEWELRY', 'KWIK',
            'KWIK SHOP', 'LOAF', 'LOAF \'N JUG', 'OWENS', 'QUIK STOP',
            'SHELL COMPANY', 'THE LITTLE CLINIC', 'TOM', 'TURKEY',
            'TURKEY HILL', 'TURKEY HILL MINIT MARKETS', 'VITACOST')]
        self.write_config('chains', 'chain_list', str(chains_list))
        return chains_list

    def get_locations(self, zip, chain, limit):
        heads = {
            "Accept": "application/json\\",
            "Authorization": "Bearer " + self.just_token,
        }
        paras = {
            "filter.zipCode.near": zip,
            "filter.chain": chain,
            "filter.limit": limit,
            "filter.radiusInMiles": 25,
        }
        self.is_token_expiring()
        return requests.get("https://api.kroger.com/v1/locations",
                            params=paras, headers=heads).json()

    def get_products(self, searchterm, limit, locID):
        heads = {
            "Accept": "application/json\\",
            "Authorization": "Bearer " + self.just_token,
        }
        params = {
            "filter.term": searchterm,
            "filter.limit": limit,
            "filter.locationId": locID,
            "filter.fulfillment": "ais",
        }
        return requests.get("https://api.kroger.com/v1/products",
                            params=params, headers=heads).json()

    # Credentials functions
    def credentials_button_event(self):
        self.client_id = self.credentials_id_entry.get()
        self.client_secret = self.credentials_secret_entry.get()
        self.write_config('auth', 'c_i', str(self.client_id))
        self.write_config('auth', 'c_s', str(self.client_secret))
        self.get_token()
        self.credentials_button.configure(
                text="Credentials Verified",
                fg_color="green", hover_color="green")
        self.chains_optionmenu.set('KROGER')
        chains_list = self.get_chains()
        self.chains_optionmenu.configure(values=chains_list)

    # Store search/select buttons functions
    def stores_search_button_event(self):
        self.is_token_expiring()
        zip = self.zip_entry.get()
        chain = self.chains_optionmenu.get()
        limit = 35
        stores_json = self.get_locations(zip, chain, limit)
        stores_list = []
        for i in range(len(stores_json.get("data"))):
            locid = str(stores_json.get("data")[i].get("locationId"))
            # Strip division number and leading zeros from location ID
            shortid = locid[locid.rfind('0', 3, 5)+1:]
            stores_list.append(stores_json.get("data")[i].get("name")
                               + " - Store #" + shortid + " (" + locid + ")")
        # Remove stores that are not retail stores
        stores_list = [i for i in stores_list if "Pickup" not in i
                       if "Walgreen" not in i if " Fuel " not in i
                       if "Warehouse" not in i]
        del stores_list[10:]  # Limit to 10 stores
        # Remove chain name from store name
        stores_list = [i[i.find(' - ')+3:] for i in stores_list]
        self.write_config('alternates', 'location_list', str(stores_list, ))
        self.write_config('location', 'user_zip', zip)
        self.stores_optionmenu.configure(values=stores_list)
        self.stores_optionmenu.set(stores_list[0])
        self.product_search_location.configure(values=stores_list)
        self.stores_select_button.configure(state=tkinter.NORMAL)

    def stores_select_button_event(self):
        self.store_selection = self.stores_optionmenu.get()
        self.store_number = self.store_selection[
            self.store_selection.find('(')
            + 1:self.store_selection.find(')')]
        self.store_name = self.store_selection[
            :self.store_selection.find(' - Store')]
        self.write_config('location', 'location_id', self.store_number)
        self.write_config('location', 'location_name', self.store_name)
        self.price_check_button.configure(state=tkinter.NORMAL)
        self.historical_prices_button.configure(state=tkinter.NORMAL)
        self.product_search_location.set(self.store_selection)
        # self.product_search_location.configure(width=500)
        self.frame_prices.lift()

    # Price check functions
    def product_search_button_event(self, event=None):
        self.is_token_expiring()
        self.store_selection = self.stores_optionmenu.get()
        self.store_number = self.store_selection[
            self.store_selection.find('(')
            + 1:self.store_selection.find(')')]
        self.product_search_term = self.product_search_bar.get()
        products = self.get_products(self.product_search_term, 20,
                                     self.store_number)
        # display products
        for widget in self.subframe_product_list.winfo_children():
            widget.destroy()
        for i in range(len(products.get('data'))):
            upc = products.get("data")[i].get('upc')
            description = products.get("data")[i].get('description')
            brand = products.get("data")[i].get('brand')
            size = products.get("data")[i].get('items')[0].get('size')
            useless_units = (' / ', 'pk', 'ct', 'pc', ' c')
            if any(term in size for term in useless_units):
                parseable_size = ''
            else:
                parseable_size = size
            parseable_size = parseable_size.replace('fl oz', 'floz')
            if 'lb' in size and 'oz' in size:
                pattern = '{lb} lb {oz} oz'
                lb_oz = self.ureg.parse_pattern(size, pattern)
                if lb_oz == []:
                    parseable_size = ''
                else:
                    parseable_size = (lb_oz[0].to(
                        self.ureg.sys.US.ounce) + lb_oz[1])
                    parseable_size = round(parseable_size, 3)
                    parseable_size = str(parseable_size)
            else:
                pass
            if parseable_size == '':
                pass
            else:
                parseable_size = self.ureg(parseable_size).to_base_units()
                try:
                    parseable_size = parseable_size.to('fluid_ounce')
                except Exception as error:
                    # print("Error: Not a fluid, apparently")
                    pass
                try:
                    parseable_size = parseable_size.to('ounce')
                except Exception as error:
                    # print("Error: Not a solid, either?")
                    pass
            sold_by = products.get("data")[i].get('items')[0].get('soldBy')
            try:
                reg_price = products.get("data")[i].get('items')[0].get(
                    'price').get('regular')
            except Exception as error:
                reg_price = 0
                print(error)
            try:
                promo_price = products.get("data")[i].get('items')[0].get(
                    'price').get('promo')
            except Exception as error:
                promo_price = 0
                print(error)
            if promo_price == 0:
                promo_price = reg_price
            percent = 0 if reg_price == 0 else int(
                (1 - (promo_price / reg_price)) * 100)
            try:
                unit_parse = parseable_size.units
                magnitude_parse = parseable_size.magnitude
                if unit_parse.dimensionless:
                    unit_parse = ''
                    magnitude_parse = ''
            except Exception as error:
                unit_parse = ''
                magnitude_parse = ''
                print(error)

            # Set today's price for items
            today = datetime.now().strftime("%Y-%m-%d")
            if upc in self.df.UPC.values:
                self.df.loc[tuple((self.df["UPC"] == upc, [today]))] = \
                    f'{reg_price}|{promo_price}'
            else:
                self.df = self.df.append({'UPC': upc, 'Brand': brand,
                                          'Description': description,
                                          'Size': size,
                                          'Sold By': sold_by,
                                          today: f'{reg_price}, {promo_price}',
                                          }, ignore_index=True)

            data = [upc, description, size, sold_by, reg_price, promo_price,
                    unit_parse, magnitude_parse, percent]
            button_text = ''.join(description + " - "
                                  + size + " - "
                                  + str("${:,.2f}".format(promo_price)))
            self.product_list_button = customtkinter.CTkButton(
                master=self.subframe_product_list,
                text=button_text,
                command=lambda data=data: self.product_info_event(data))
            self.product_list_button.grid(row=i, column=0, columnspan=2,
                                          sticky="nswe", padx=10, pady=5)
        self.df.to_csv('pricing-data.csv.xz', index=False)

    def product_info_event(self, data):
        for widget in self.subframe_product_info.winfo_children():
            widget.destroy()

        self.info_desc = customtkinter.CTkLabel(
            master=self.subframe_product_info, text=data[1],
            text_font=("", -18))
        self.info_desc.grid(row=0, column=0, columnspan=2,
                            padx=2, pady=15)

        self.info_upc = customtkinter.CTkLabel(
            master=self.subframe_product_info,
            text="UPC: " + data[0],
            justify="left",
            anchor="w",
            text_font=("", -14))
        self.info_upc.grid(row=1, column=0, sticky="nswe",
                           padx=5, pady=5)

        self.info_size = customtkinter.CTkLabel(
            master=self.subframe_product_info,
            text="Size: " + data[2],
            justify="left",
            anchor="w",
            text_font=("", -14))
        self.info_size.grid(row=2, column=0, sticky="nswe",
                            padx=5, pady=5)

        self.info_soldby = customtkinter.CTkLabel(
            master=self.subframe_product_info,
            text="Sold by: " + data[3].lower(),
            justify="left",
            anchor="w",
            text_font=("", -14))
        self.info_soldby.grid(row=3, column=0, sticky="nswe",
                              padx=5, pady=5)

        self.info_reg_price = customtkinter.CTkLabel(
            master=self.subframe_product_info,
            text="Regular price: " + str("${:,.2f}".format(data[4])),
            justify="left",
            anchor="w",
            text_font=("", -14))
        self.info_reg_price.grid(row=4, column=0, sticky="nswe",
                                 padx=5, pady=5)

        self.info_promo_price = customtkinter.CTkLabel(
            master=self.subframe_product_info,
            text="Promo price: " + str("${:,.2f}".format(data[5])),
            justify="left",
            anchor="w",
            text_font=("", -14))
        self.info_promo_price.grid(row=5, column=0, sticky="nswe",
                                   padx=5, pady=5)

        if data[7] == '':
            unit_price = "Unable to compute"
        else:
            unit_price = str("${:,.3f}".format(
                (float(data[5]) / float(data[7])))) + "/" + str(f"{data[6]:~}")

        self.info_unit_price = customtkinter.CTkLabel(
            master=self.subframe_product_info,
            text="Unit price: " + unit_price,
            justify="left",
            anchor="w",
            text_font=("", -14))
        self.info_unit_price.grid(row=6, column=0, sticky="nswe",
                                  padx=5, pady=5)

        self.info_percent = customtkinter.CTkLabel(
            master=self.subframe_product_info,
            text="Percent discounted: " + str(data[8]) + "%",
            justify="left",
            anchor="w",
            text_font=("", -14))
        self.info_percent.grid(row=7, column=0, sticky="nswe",
                               padx=5, pady=5)

        # Get photo; Kroger web server redirects to never-ending 404 page
        picURL = "https://www.kroger.com/product/images/medium/front/" \
            + data[0]
        try:
            response = requests.get(picURL, stream=all, verify=True, timeout=2)
            if response.ok:
                header_byte = response.content[0:3].hex()
                if header_byte == 'ffd8ff':
                    image = Image.open(BytesIO(response.content))
                else:
                    image = Image.open("no_image.jpg")
            else:
                image = Image.open("no_image.jpg")
        except Exception as e:
            image = Image.open("no_image.jpg")
            print(e)
        tkphoto = ImageTk.PhotoImage(image)

        self.info_picture = customtkinter.CTkLabel(
            master=self.subframe_product_info,
            image=tkphoto)
        self.info_picture.image = tkphoto
        self.info_picture.grid(row=1, column=1, sticky="nswe",
                               padx=5, pady=5, rowspan=7)

        # Plot the historical data
        single = self.df[self.df['UPC'] == data[0]].drop(
            self.df.columns[[range(5)]], axis=1)
        split = single.apply(
            lambda x: x.str.split('|').explode()).reset_index()
        split = split.drop(split.columns[0], axis=1)
        split = split.astype('float')
        split = split.transpose()
        split.rename(columns={0: 'Regular', 1: 'Promo'}, inplace=True)

        fig = Figure(figsize=(7, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.yaxis.set_major_formatter('${x:1.2f}')

        split.plot(style=['ro-', 'b^-'], linewidth=2.0, ax=ax)

        canvas = FigureCanvasTkAgg(fig, master=self.subframe_product_info,)
        # canvas.show()
        canvas.get_tk_widget().grid(row=8, column=0, columnspan=2)

    # Application functions
    def change_mode(self):
        if self.dark_mode_switch.get() == 1:
            customtkinter.set_appearance_mode("dark")
            self.state("zoomed")
            self.iconbitmap('price_check_dark.ico')
        else:
            customtkinter.set_appearance_mode("light")
            self.state("zoomed")
            self.iconbitmap('price_check.ico')

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()

    def write_config(self, section, key, value):
        config = configparser.ConfigParser()
        config.read('config.ini')
        if config.has_section(section):
            pass
        else:
            config.add_section(section)
        config.set(section, key, value)
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    def read_list(self, section, key):
        config = configparser.ConfigParser()
        config.read('config.ini')
        list = config.get(section, key)
        list = list[1:-1]
        list = list.split(',')
        list = [e.strip() for e in list]
        list = [e[1:-1] for e in list]
        return list

    # Navigation button functions
    def prices_button_event(self):
        self.frame_prices.lift()

    def historical_button_event(self):
        self.frame_historical_prices.lift()

    def settings_button_event(self):
        self.frame_settings.lift()

    # Settings loader
    def load_settings(self):
        # Load settings from ini file and the API
        readconfig = None
        readconfig = configparser.ConfigParser()

        if readconfig.read('config.ini') == []:
            pass

        else:
            # read values
            self.client_id = readconfig.get('auth', 'c_i')
            self.client_secret = readconfig.get('auth', 'c_s')
            self.token_exp = readconfig.get('token', 'token_exp')
            self.just_token = readconfig.get('token', 'just_token')
            self.store_number = str(readconfig.get('location', 'location_id'))
            self.store_name = str(readconfig.get('location', 'location_name'))
            self.zip = str(readconfig.get('location', 'user_zip'))
            self.stores_list = self.read_list('alternates', 'location_list')

            # set values to settings frame
            self.credentials_id_entry.insert(END, self.client_id)
            self.credentials_secret_entry.insert(END, self.client_secret)
            self.zip_entry.insert(END, self.zip)
            self.stores_optionmenu.configure(values=self.stores_list)
            self.product_search_location.configure(values=self.stores_list)

            locid = self.store_number
            shortid = locid[locid.rfind('0', 3, 5)+1:]
            set_store = self.store_name + " - Store #" + shortid \
                + " (" + locid + ")"

            self.stores_optionmenu.set(set_store)
            # self.stores_optionmenu.set(self.store_name)
            self.product_search_location.set(set_store)

            self.is_token_expiring()

            self.credentials_button.configure(
                text="Credentials Verified",
                fg_color="green", hover_color="green")

            # Get list of chains and populate chains optionmenu
            self.chains_optionmenu.set('KROGER')
            chains_list = self.read_list('chains', 'chain_list')
            self.chains_optionmenu.configure(values=chains_list)

            self.stores_select_button.configure(state=tkinter.NORMAL)
            self.price_check_button.configure(state=tkinter.NORMAL)
            self.historical_prices_button.configure(state=tkinter.NORMAL)
            self.frame_prices.lift()

        self.df = pd.read_csv('pricing-data.csv.xz',
                              converters={'UPC': str, })


if __name__ == "__main__":
    app = App()
    app.start()
