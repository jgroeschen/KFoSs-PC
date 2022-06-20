import configparser
import time
import tkinter
import tkinter.messagebox
from tkinter import END

import customtkinter
from oauthlib.oauth2 import BackendApplicationClient
import requests
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

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
        self.frame_prices.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        # self.frame_prices.columnconfigure(2, weight=0)

        self.product_search_bar = customtkinter.CTkEntry(
            master=self.frame_prices)
        self.product_search_bar.grid(row=0, column=0, columnspan=6,
                                     sticky="nswe", padx=10, pady=10)

        self.product_search_location = customtkinter.CTkOptionMenu(
            master=self.frame_prices,)
        self.product_search_location.grid(row=0, column=6, sticky="nswe",
                                          padx=10, pady=10)

        self.product_search_button = customtkinter.CTkButton(
            master=self.frame_prices, text="Search",
            command=self.product_search_button_event)
        self.product_search_button.grid(row=0, column=7, sticky="nswe",
                                        padx=10, pady=10)

        self.subframe_product_list = customtkinter.CTkFrame(
            master=self.frame_prices)
        self.subframe_product_list.grid(row=1, column=0, columnspan=4,
                                        sticky="nswe", padx=10, pady=10)

        self.subframe_product_info = customtkinter.CTkFrame(
            master=self.frame_prices)
        self.subframe_product_info.grid(row=1, column=4, columnspan=4,
                                        pady=10, padx=10, sticky="nsew")

        '''
        #Very Temporary
        rows = []

        for i in range(6):

            cols = []

            for j in range(8):

                e = customtkinter.CTkEntry(master=self.frame_info)

                e.grid(row=i, column=j, sticky='NSEW')

                e.insert(END, 'row %d, column %d' % (i, j))
                e.configure(state='disabled')

                cols.append(e)

            rows.append(cols)
        '''

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
            text="Check your credentials",)
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
            master=self.settings_subframe_stores, values=[''])
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
        return requests.get("https://api.kroger.com/v1/locations",
                            params=paras, headers=heads).json()

    # Store search/select buttons functions
    def stores_search_button_event(self):
        print("Stores button pressed")
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
        self.stores_optionmenu.configure(values=stores_list)
        self.product_search_location.configure(values=stores_list)
        self.stores_select_button.configure(state=tkinter.NORMAL)

    def stores_select_button_event(self):
        self.store_selection = self.stores_optionmenu.get()
        self.store_number = self.store_selection[
            self.store_selection.find('(')
            + 1:self.store_selection.find(')')]
        self.store_name = self.store_selection[
            :self.store_selection.find(' - Store')]
        self.price_check_button.configure(state=tkinter.NORMAL)
        self.historical_prices_button.configure(state=tkinter.NORMAL)
        self.product_search_location.set(self.store_selection)
        self.frame_prices.lift()

    # Price check functions
    def product_search_button_event(self):
        print("Product search button pressed")

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

    # Navigation button functions
    def prices_button_event(self):
        print("Prices button pressed")
        self.frame_prices.lift()

    def historical_button_event(self):
        print("Historical button pressed")
        self.frame_historical_prices.lift()

    def settings_button_event(self):
        print("Settings button pressed")
        self.frame_settings.lift()

    # Settings loader
    def load_settings(self):
        # Load settings from ini file and the API
        readconfig = None
        readconfig = configparser.ConfigParser()

        if readconfig.read('config.ini') == []:
            self.client_id = ''
            self.client_secret = ''
            self.token_exp = ''
            self.just_token = ''
            self.store_number = ''

        else:
            self.client_id = readconfig.get('auth', 'c_i')
            self.client_secret = readconfig.get('auth', 'c_s')
            self.token_exp = readconfig.get('token', 'token_exp')
            self.just_token = readconfig.get('token', 'just_token')
            self.store_number = str(readconfig.get('location', 'location_id'))
            self.store_name = str(readconfig.get('location', 'location_name'))
            print(self.just_token)
            self.get_token()

            self.credentials_id_entry.insert(END, self.client_id)
            self.credentials_secret_entry.insert(END, self.client_secret)
            # self.stores_optionmenu.set(self.store_name)
            self.credentials_button.configure(
                text="Credentials Verified",
                fg_color="green", hover_color="green")

            # Get list of chains and populate chains optionmenu
            self.chains_optionmenu.set('KROGER')
            chains_list = self.get_chains()
            self.chains_optionmenu.configure(values=chains_list)


if __name__ == "__main__":
    app = App()
    app.start()
