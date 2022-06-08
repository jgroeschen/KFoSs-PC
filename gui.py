import configparser
import tkinter
import tkinter.messagebox
from tkinter import END
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()


        # Configure the window
        self.title("KFoSs-PC -- The Kroger Family of Stores Price Checker")
        self.iconbitmap('price_check_dark.ico')

        self.minsize(960,540)
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        self.state('zoomed')

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        


        # Create a grid to hold left and right side frames ============================================================
        self.grid_columnconfigure(0, weight=0, minsize=200)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create the frames
        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 corner_radius=5)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_prices = customtkinter.CTkFrame(master=self)
        self.frame_prices.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

        self.frame_historical_prices = customtkinter.CTkFrame(master=self)
        self.frame_historical_prices.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

        self.frame_closeouts = customtkinter.CTkFrame(master=self)
        self.frame_closeouts.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

        self.frame_settings = customtkinter.CTkFrame(master=self)
        self.frame_settings.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)


        # Create and arrange frame_left
        self.frame_left.grid_rowconfigure(0, minsize=10) 
        self.frame_left.grid_rowconfigure(2, minsize=10) 
        self.frame_left.grid_rowconfigure(18, weight=1)
        self.frame_left.grid_rowconfigure(19, minsize=20) 
        self.frame_left.grid_rowconfigure(21, minsize=10)

        self.left_title = customtkinter.CTkLabel(master=self.frame_left,
                                              text="KFoSs-PC",
                                              text_font=("Roboto Medium", -24))
        self.left_title.grid(row=1, pady=10, padx=10)

        self.price_check_button = customtkinter.CTkButton(master=self.frame_left,
                                                text="Price Checker",
                                                text_font=("Roboto", -18),
                                                fg_color=("gray70", "gray30"),
                                                command=self.button_event)
        self.price_check_button.grid(row=3, pady=10, padx=10, ipadx=10, ipady=5, sticky="we")
        self.price_check_button.configure(state=tkinter.DISABLED)

        self.historical_prices_button = customtkinter.CTkButton(master=self.frame_left,
                                                text="Historical Prices",
                                                text_font=("Roboto", -18),
                                                fg_color=("gray70", "gray30"),
                                                command=self.button_event)
        self.historical_prices_button.grid(row=4, pady=10, padx=10, ipadx=10, ipady=5, sticky="we")
        self.historical_prices_button.configure(state=tkinter.DISABLED)

        self.settings_button = customtkinter.CTkButton(master=self.frame_left,
                                                text="Settings",
                                                text_font=("Roboto", -18),
                                                fg_color=("gray70", "gray30"),
                                                command=self.settings_button_event)
        self.settings_button.grid(row=5, pady=10, padx=10, ipadx=10, ipady=5, sticky="we")

        self.dark_mode_switch = customtkinter.CTkSwitch(master=self.frame_left,
                                                text="Dark Mode",
                                                command=self.change_mode)
        self.dark_mode_switch.grid(row=20, pady=10, padx=20, sticky="w")
        self.dark_mode_switch.select()


        # Create and arrange frame_prices
        self.frame_prices.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_prices.rowconfigure(7, weight=10)
        self.frame_prices.columnconfigure((0, 1), weight=1)
        self.frame_prices.columnconfigure(2, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_prices)
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=4, pady=20, padx=20, sticky="nsew")

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


        # Create and arrange frame_historical_prices


        # Create and arrange frame_closeouts


        # Create and arrange frame_settings
        self.frame_settings.grid_rowconfigure(0, minsize=10)
        self.frame_settings.grid_rowconfigure(2, minsize=10)
        self.frame_settings.grid_rowconfigure(4, minsize=10)
        
        self.settings_title = customtkinter.CTkLabel(master=self.frame_settings,
                                              text="KFoSs-PC Settings",
                                              text_font=("Roboto Medium", -24))  
        self.settings_title.grid(row=1, column=0, pady=10, padx=10)

        # Create and arrange settings_subframe_credentials
        self.settings_subframe_credentials = customtkinter.CTkFrame(master=self.frame_settings)
        self.settings_subframe_credentials.grid(row=3, column=0, sticky="nswe", padx=20, pady=10)

        self.credentials_title = customtkinter.CTkLabel(master=self.settings_subframe_credentials,
                                              text="Credentials",
                                              text_font=("Roboto Medium", -24))  
        self.credentials_title.grid(row=0, column=0, columnspan=3, sticky="nswe", padx=20, pady=20)

        self.credentials_id_label = customtkinter.CTkLabel(master=self.settings_subframe_credentials,
                                                        text="Enter your ID:")
        self.credentials_id_label.grid(row=1, column=0, sticky="w", padx=20, pady=20)

        self.credentials_id_entry = customtkinter.CTkEntry(master=self.settings_subframe_credentials)
        self.credentials_id_entry.grid(row=1, column=1, sticky="w", padx=20, pady=20)

        self.credentials_secret_label = customtkinter.CTkLabel(master=self.settings_subframe_credentials,
                                                        text="Enter your Secret:")
        self.credentials_secret_label.grid(row=3, column=0, sticky="w", padx=20, pady=20)

        self.credentials_secret_entry = customtkinter.CTkEntry(master=self.settings_subframe_credentials, show="*")
        self.credentials_secret_entry.grid(row=3, column=1, sticky="w", padx=20, pady=20)

        self.credentials_button = customtkinter.CTkButton(master=self.settings_subframe_credentials, text="Check your credentials",)
        self.credentials_button.grid(row=1, column=3, rowspan=3, sticky="nswe", padx=20, pady=20)

        # Create and arrange settings_subframe_stores
        self.settings_subframe_stores = customtkinter.CTkFrame(master=self.frame_settings)
        self.settings_subframe_stores.grid(row=5, column=0, sticky="nswe", padx=20, pady=10)

        self.stores_title = customtkinter.CTkLabel(master=self.settings_subframe_stores,
                                              text="My Store",
                                              text_font=("Roboto Medium", -24))  
        self.stores_title.grid(row=0, column=0, columnspan=3, sticky="nswe", padx=20, pady=20)

        self.zip_label = customtkinter.CTkLabel(master=self.settings_subframe_stores, text="Enter your ZIP:").grid(row=1, column=0, sticky="w", padx=20, pady=20)

        self.zip_entry = customtkinter.CTkEntry(master=self.settings_subframe_stores)
        self.zip_entry.grid(row=1, column=1, sticky="nswe", padx=20, pady=20)

        #self.stores_combobox = customtkinter.CTkComboBox(master=self.settings_subframe_stores)
        #self.stores_combobox.grid(row=2, column=0, columnspan=2, sticky="nswe", padx=20, pady=20)

        self.stores_optionmenu = customtkinter.CTkOptionMenu(master=self.settings_subframe_stores,values=[''])
        self.stores_optionmenu.grid(row=3, column=0, columnspan=2, sticky="nswe", padx=20, pady=20)

        self.stores_optionmenu.configure(values=["option 1", "option 2", "option 3"]) #Temporary testing configuration for optionmenu

        self.stores_search_button = customtkinter.CTkButton(master=self.settings_subframe_stores, text="Find nearby stores", command=self.stores_search_button_event)
        self.stores_search_button.grid(row=1, column=3, rowspan=1, sticky="nswe", padx=20, pady=20)

        self.stores_select_button = customtkinter.CTkButton(master=self.settings_subframe_stores, text="Select this store", command=self.stores_select_button_event)
        self.stores_select_button.grid(row=3, column=3, rowspan=1, sticky="nswe", padx=20, pady=20)
        self.stores_select_button.configure(state="disabled")








        # Load Settings
        self.protocol('WM_TAKE_FOCUS', self.load_settings())


    




    def button_event(self):
        print("Button pressed")
        
        
        self.frame_prices.lift()

    def settings_button_event(self):
        print("Settings button pressed")
        self.frame_settings.lift()
    
    def stores_search_button_event(self):
        print("Stores button pressed")

        self.stores_select_button.configure(state=tkinter.NORMAL)

    def stores_select_button_event(self):
        print("Stores select button pressed")
        self.price_check_button.configure(state=tkinter.NORMAL)
        self.historical_prices_button.configure(state=tkinter.NORMAL)
       
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


    def load_settings(self):
        # Load settings from file
        readconfig = configparser.ConfigParser()

        if readconfig.read('config.ini') == None:
            c_i = ''
            c_s = ''
            token_exp = ''
            just_token = ''
            storenumber = ''

        else:
            c_i = readconfig.get('auth','c_i')
            c_s = readconfig.get('auth','c_s')  
            token_exp = readconfig.get('token', 'token_exp')
            just_token = readconfig.get('token', 'just_token')
            storenumber = str(readconfig.get('location', 'location_id'))
            self.credentials_id_entry.insert(END, c_i)
            self.credentials_secret_entry.insert(END, c_s)
            self.stores_optionmenu.set(storenumber)
            self.stores_optionmenu.configure(values=[storenumber])
            self.credentials_button.configure(text="Credentials Verified", fg_color="green", hover_color="green")
    
    




if __name__ == "__main__":
    app = App()
    app.start()