import customtkinter as ctk
import webbrowser
from datetime import datetime
import request_api
import threading
from PIL import Image, ImageTk
from io import BytesIO
import requests

provinces_in_philippines = {
    "NCR": ["Manila"],
    "CAR": ["Abra", "Apayao", "Kalinga"],
    "Region I": ["Ilocos Norte", "Ilocos Sur", "La Union", "Pangasinan"],
    "Region II": ["Batanes", "Cagayan", "Isabela", "Nueva Vizcaya", "Quirino"],
    "Region III": ["Aurora", "Bataan", "Bulacan", "Nueva Ecija", "Pampanga", "Tarlac", "Zambales"],
    "Region IV-A": ["Batangas", "Cavite", "Laguna", "Quezon", "Rizal"],
    "Region IV-B": ["Marinduque", "Occidental Mindoro", "Palawan", "Romblon"],
    "Region V": ["Albay", "Camarines Norte", "Camarines Sur", "Catanduanes", "Masbate", "Sorsogon"],
    "Region VI": ["Aklan", "Antique", "Capiz", "Guimaras", "Iloilo", "Negros Occidental"],
    "Region VII": ["Bohol", "Cebu", "Siquijor"],
    "Region VIII": ["Biliran", "Leyte", "Samar", "Southern Leyte"],
    "Region IX": ["Zamboanga del Norte", "Zamboanga del Sur", "Zamboanga Sibugay"],
    "Region X": ["Bukidnon", "Camiguin", "Lanao del Norte", "Misamis Occidental", "Misamis Oriental"],
    "Region XI": ["Davao de Oro", "Davao del Norte", "Davao del Sur", "Davao Occidental", "Davao Oriental"],
    "Region XII": ["Cotabato (North Cotabato)", "Sarangani", "South Cotabato", "Sultan Kudarat"],
    "Region XIII": ["Agusan del Norte", "Agusan del Sur", "Dinagat Islands", "Surigao del Norte", "Surigao del Sur"],
    "BARMM": ["Basilan", "Lanao del Sur", "Maguindanao del Norte", "Maguindanao del Sur", "Sulu", "Tawi-Tawi"]
}

def update_time():
    current_time = datetime.now().strftime("%H:%M %p")
    current_date = datetime.now()
    formatted_date = current_date.strftime("%A, %d %B %Y")

    app.label1.configure(text=current_time, font=('Leelawadee UI Semilight', 50))
    app.label2.configure(text=formatted_date, font=('Leelawadee UI Semilight', 17))

    app.after(1000, update_time)


def open_website_api():
    url = 'https://www.weatherbit.io/'
    webbrowser.open(url)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("790x500")
        self.title("Ram's Weather App")
        self.iconbitmap('./logo_ni_ram2.ico')
        self.resizable(False, False)
        self.selected_city = ''

        self.main_frame = ctk.CTkFrame(
            self, 
            fg_color="#0B131E"
        )
        self.main_frame.pack(
            fill="both", 
            expand=True
        )

        self.checkbox_frame1 = ctk.CTkFrame(
            self, 
            width=250, 
            height=300, 
            corner_radius=20, 
            fg_color='#202B3C', 
            bg_color='#0B131E'
        )
        self.checkbox_frame1.place(
            x=20, 
            y=20
        )

        self.checkbox_frame2 = ctk.CTkFrame(
            self, 
            width=750, 
            height=130, 
            corner_radius=20, 
            fg_color='#202B3C', 
            bg_color='#0B131E'
        )
        self.checkbox_frame2.place(
            x=20, 
            y=345
        )

        self.region_var = ctk.StringVar(
            value="Select Region"
        )
        self.combobox1 = ctk.CTkOptionMenu(
            self, 
            variable=self.region_var, 
            values=list(provinces_in_philippines.keys()), 
            width=210, 
            height=35, 
            fg_color='#0B131E', 
            button_color='#35455F', 
            button_hover_color='#0B131E', 
            font=('Leelawadee UI Semilight', 15)
        )
        self.combobox1.place(
            x=40, 
            y=170
        )
        self.region_var.trace_add("write", self.update_city)

        self.city_var = ctk.StringVar(
            value="Select City"
        )
        self.combobox2 = ctk.CTkOptionMenu(
            self, 
            variable=self.city_var, 
            values=[], 
            width=210, 
            height=35, 
            fg_color='#0B131E', 
            button_color='#35455F', 
            button_hover_color='#0B131E', 
            font=('Leelawadee UI Semilight', 15)
        )
        self.combobox2.place(
            x=40, 
            y=220
        )

        self.get_city_button = ctk.CTkButton(
            self, 
            text="Get Weather", 
            command=self.get_city, 
            width=210, 
            height=35, 
            corner_radius=30, 
            fg_color='#0B131E', 
            bg_color='#202B3C', 
            font=('Leelawadee UI Semilight', 15)
        )
        self.get_city_button.place(
            x=40, 
            y=270
        )

        self.label1 = ctk.CTkLabel(
            self, 
            text="", 
            fg_color="#202B3C", 
            font=('Leelawadee UI Semilight', 50)
        )
        self.label1.place(
            x=44, 
            y=40
        )

        self.label2 = ctk.CTkLabel(
            self, 
            text='', 
            fg_color="#202B3C", 
            font=('Leelawadee UI Semilight', 17)
        )
        self.label2.place(
            x=38, 
            y=110
        )

        self.label3 = ctk.CTkLabel(
            self, 
            text='', 
            fg_color="#0B131E", 
            font=('Leelawadee UI Semilight', 40)
        )
        self.label3.place(
            x=600, 
            y=30
        )

        self.label4 = ctk.CTkLabel(
            self, 
            text=(f'{self.selected_city}'), 
            fg_color="#0B131E", 
            anchor="e", 
            font=('Leelawadee UI Semilight', 25), 
            justify='right'
        )
        self.label4.place(
            x=707, 
            y=83
        )

        self.label5 = ctk.CTkLabel(
            self, 
            text='', 
            fg_color="#0B131E", 
            font=('Bahnschrift SemiBold SemiConden', 50)
        )
        self.label5.place(
            x=695, 
            y=120
        )

        self.logo = ctk.CTkLabel(
            self, 
            text='',
            image=self.get_logo(),
            bg_color='#0B131E'
        )
        self.logo.place(
            x=290,
            y=100
        )

        self.mon = ctk.CTkLabel(
            self, 
            text='', 
            fg_color="#202B3C", 
            bg_color="#202B3C"
        )
        self.mon.place(
            x=70, 
            y=425
        )
        self.montemp = ctk.CTkLabel(
            self, 
            text='', 
            fg_color="#202B3C", 
            bg_color="#202B3C"
        )
        self.montemp.place(
            x=78, 
            y=394
        )
        self.monicon = ctk.CTkLabel(
            self, 
            text='', 
            fg_color="#202B3C", 
            bg_color="#202B3C"
        )
        self.monicon.place(
            x=69, 
            y=357
        )

        self.tues = ctk.CTkLabel(
            self, 
            text='', 
            fg_color="#202B3C", 
            bg_color="#202B3C"
        )
        self.tues.place(
            x=170, 
            y=425
        )
        self.tuestemp = ctk.CTkLabel(
            self, 
            text='', 
            fg_color="#202B3C", 
            bg_color="#202B3C"
        )
        self.tuestemp.place(
            x=176, 
            y=394
        )
        self.tuesicon = ctk.CTkLabel(
            self, 
            text='', 
            fg_color="#202B3C", 
            bg_color="#202B3C"
        )
        self.tuesicon.place(
            x=176-9, 
            y=357
        )

        self.wed = ctk.CTkLabel(
            self, 
            text='', 
            fg_color="#202B3C", 
            bg_color="#202B3C"
        )
        self.wed.place(
            x=270, 
            y=425
        )
        self.wedtemp = ctk.CTkLabel(
            self, 
            text='', 
            fg_color="#202B3C", 
            bg_color="#202B3C"
        )
        self.wedtemp.place(
            x=277, 
            y=394
        )
        self.wedicon = ctk.CTkLabel(
            self, 
            text='', 
            fg_color="#202B3C", 
            bg_color="#202B3C"
        )
        self.wedicon.place(
            x=277-9, 
            y=357
        )

        self.thurs = ctk.CTkLabel(
            self, 
            text='', 
            fg_color="#202B3C", 
            bg_color="#202B3C"
        )
        self.thurs.place(
            x=370, 
            y=425
        )
        self.thurstemp = ctk.CTkLabel(
            self, 
            text='', 
            fg_color="#202B3C", 
            bg_color="#202B3C"
        )
        self.thurstemp.place(
            x=374, 
            y=394
        )
        self.thursicon = ctk.CTkLabel(
            self, 
            text='', 
            fg_color="#202B3C", 
            bg_color="#202B3C"
        )
        self.thursicon.place(
            x=374-9, 
            y=357
        )

        self.fri = ctk.CTkLabel(
            self, 
            text='', 
            fg_color="#202B3C", 
            bg_color="#202B3C"
        )
        self.fri.place(
            x=480, 
            y=425
        )
        self.fritemp = ctk.CTkLabel(
            self, 
            text='', 
            fg_color="#202B3C", 
            bg_color="#202B3C"
        )
        self.fritemp.place(
            x=481, 
            y=394
        )
        self.friicon = ctk.CTkLabel(
            self, 
            text='', 
            fg_color="#202B3C", 
            bg_color="#202B3C"
        )
        self.friicon.place(
            x=481-9, 
            y=357
        )

        self.sat = ctk.CTkLabel(
            self, 
            text='', 
            fg_color="#202B3C", 
            bg_color="#202B3C"
        )
        self.sat.place(
            x=580, 
            y=425
        )
        self.sattemp = ctk.CTkLabel(
            self, 
            text='', 
            fg_color="#202B3C", 
            bg_color="#202B3C"
        )
        self.sattemp.place(
            x=582, 
            y=394
        )
        self.saticon = ctk.CTkLabel(
            self, 
            text='', 
            fg_color="#202B3C", 
            bg_color="#202B3C"
        )
        self.saticon.place(
            x=582-9, 
            y=357
        )

        self.sun = ctk.CTkLabel(
            self, 
            text='', 
            fg_color="#202B3C", 
            bg_color="#202B3C"
        )
        self.sun.place(
            x=680, 
            y=425
        )
        self.suntemp = ctk.CTkLabel(
            self, 
            text='', 
            fg_color="#202B3C", 
            bg_color="#202B3C"
        )
        self.suntemp.place(
            x=684, 
            y=394
        )
        self.sunicon = ctk.CTkLabel(
            self, 
            text='', 
            fg_color="#202B3C", 
            bg_color="#202B3C"
        )
        self.sunicon.place(
            x=684-9, 
            y=357
        )


    def update_city(self, *args):
        selected_region = self.region_var.get()
        if selected_region in provinces_in_philippines:
            cities = provinces_in_philippines[selected_region]
            self.combobox2.configure(values=cities)
            self.city_var.set("Select City") 

    def get_text_width(self, text, font):
        temp_label = ctk.CTkLabel(
            self, 
            text=text, 
            font=font)
        
        temp_label.update_idletasks()
        return temp_label.winfo_reqwidth()

    def get_city(self):

        self.show_progress_bar()
    
        def fetch_weather_data():
            self.selected_city = self.city_var.get()
            timezone, last_observed, wind_speed, temp, temp_feelslike, cloud_cvrg, precipitation, curr_weather = request_api.current_weather_req(self.selected_city, 'PH')

            self.label5.configure(
                text=f'{round(temp)}°', 
                font=('Bahnschrift SemiBold SemiConden', 50))
            
            self.label4.configure(
                text=f'{self.selected_city}', 
                font=('Leelawadee UI Semilight', 25))
            
            self.label3.configure(
                text=f'{curr_weather}', 
                font=('Leelawadee UI Semilight', 40))

            text_width = self.get_text_width(
                self.selected_city, 
                ('Leelawadee UI Semilight', 25))
            text_width2 = self.get_text_width(
                curr_weather, 
                ('Leelawadee UI Semilight', 40))

            if text_width > 0:
                self.label4.place(x=760 - text_width, y=83)

            if text_width2 > 0:
                self.label3.place(x=760 - text_width2, y=30)

            self.days = []
            self.temperatures = []
            self.descriptions = []
            self.icons = []

            self.daily_data = request_api.daily_weather(self.selected_city,'PH')
            for weather in self.daily_data['data']:
                date = weather['valid_date']
                temperature = weather['temp']
                description = weather['weather']['description']
                desc_icon = weather['weather']['icon']
                self.days.append(self.get_day_of_week(date))
                self.temperatures.append(temperature)
                self.descriptions.append(description)
                self.icons.append(desc_icon)

            starting_day = self.get_day_of_week(self.daily_data['data'][0]['valid_date'])

            day_index_map = {
                'Monday': 0,
                'Tuesday': 1,
                'Wednesday': 2,
                'Thursday': 3,
                'Friday': 4,
                'Saturday': 5, 
                'Sunday': 6
            }

            start_idx = day_index_map[starting_day]

            for i in range(min(7, len(self.days))):
                label_index = (start_idx + i) % 7
                day_abbr = self.days[i][:3]

                day_labels = [self.mon, 
                              self.tues, 
                              self.wed, 
                              self.thurs, 
                              self.fri, 
                              self.sat, 
                              self.sun]
                
                temp_labels = [self.montemp, 
                               self.tuestemp, 
                               self.wedtemp, 
                               self.thurstemp, 
                               self.fritemp, 
                               self.sattemp, 
                               self.suntemp]
                
                icon_labels = [self.monicon, 
                               self.tuesicon, 
                               self.wedicon, 
                               self.thursicon, 
                               self.friicon, 
                               self.saticon, 
                               self.sunicon]
                
                day_labels[label_index].configure(
                    text=f"{day_abbr}",
                    font=('Leelawadee UI Semilight', 20)
                )
                temp_labels[label_index].configure(
                    text=f"{round(self.temperatures[i])}°",
                    font=('Bahnschrift SemiBold SemiConden', 20))
                
                icon_img = self.get_api_image(self.icons[i])

                if icon_img:
                    icon_labels[label_index].configure(image=icon_img)
                    icon_labels[label_index].image = icon_img  
                
            self.hide_progress_bar()

        threading.Thread(target=fetch_weather_data).start()

    def get_day_of_week(self, date_str):
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%A")
    
    def progress_bar_load(self):

        self.progress_bar = ctk.CTkProgressBar(
            self, 
            width=150,
            height=12, 
            orientation='horizontal',
            mode='indeterminate',
            progress_color='#35455F',
            fg_color='#0B131E')

    def show_progress_bar(self):
        self.progress_bar.place(x=70, y=145)
        self.progress_bar.start()
        self.update_idletasks()

    def hide_progress_bar(self):
        self.progress_bar.stop()
        self.progress_bar.place_forget()
    
    def get_api_image(self, icon_code):
        base_url = "https://www.weatherbit.io/static/img/icons/"
        img_url = f"{base_url}{icon_code}.png"
        
        response = requests.get(img_url)
        image_data = BytesIO(response.content)
        img = Image.open(image_data)

        img = img.resize((40, 40), Image.BOX)
        img = ImageTk.PhotoImage(img)
        return img
    
    def get_logo(self):

        imglogo = Image.open("./logo_ni_ram.png")
        imglogo = imglogo.resize((200, 200), Image.BOX)
        imglogo = ImageTk.PhotoImage(imglogo)
        return imglogo

        
app = App()
app.progress_bar_load()
update_time()
app.mainloop()