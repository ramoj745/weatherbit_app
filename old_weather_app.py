from tkinter import *
from PIL import Image, ImageTk
from request_api import current_weather_req
import webbrowser
import tkinter as tk
from tkinter import ttk


provinces_in_philippines = {
    "NCR": ["Manila"],
    "CAR": [
        "Abra",
        "Apayao",
        "Benguet",
        "Ifugao",
        "Kalinga"
    ],
    "Region I": [
        "Ilocos Norte",
        "Ilocos Sur",
        "La Union",
        "Pangasinan"
    ],
    "Region II": [
        "Batanes",
        "Cagayan",
        "Isabela",
        "Nueva Vizcaya",
        "Quirino"
    ],
    "Region III": [
        "Aurora",
        "Bataan",
        "Bulacan",
        "Nueva Ecija",
        "Pampanga",
        "Tarlac",
        "Zambales"
    ],
    "Region IV-A": [
        "Batangas",
        "Cavite",
        "Laguna",
        "Quezon",
        "Rizal"
    ],
    "Region IV-B": [
        "Marinduque",
        "Occidental Mindoro",
        "Oriental Mindoro",
        "Palawan",
        "Romblon"
    ],
    "Region V": [
        "Albay",
        "Camarines Norte",
        "Camarines Sur",
        "Catanduanes",
        "Masbate",
        "Sorsogon"
    ],
    "Region VI": [
        "Aklan",
        "Antique",
        "Capiz",
        "Guimaras",
        "Iloilo",
        "Negros Occidental"
    ],
    "Region VII": [
        "Bohol",
        "Cebu",
        "Siquijor"
    ],
    "Region VIII": [
        "Biliran",
        "Eastern Samar",
        "Leyte",
        "Samar",
        "Southern Leyte"
    ],
    "Region IX": [
        "Zamboanga del Norte",
        "Zamboanga del Sur",
        "Zamboanga Sibugay"
    ],
    "Region X": [
        "Bukidnon",
        "Camiguin",
        "Lanao del Norte",
        "Misamis Occidental",
        "Misamis Oriental"
    ],
    "Region XI": [
        "Davao de Oro",
        "Davao del Norte",
        "Davao del Sur",
        "Davao Occidental",
        "Davao Oriental"
    ],
    "Region XII": [
        "Cotabato (North Cotabato)",
        "Sarangani",
        "South Cotabato",
        "Sultan Kudarat"
    ],
    "Region XIII": [
        "Agusan del Norte",
        "Agusan del Sur",
        "Dinagat Islands",
        "Surigao del Norte",
        "Surigao del Sur"
    ],
    "BARMM": [
        "Basilan",
        "Lanao del Sur",
        "Maguindanao del Norte",
        "Maguindanao del Sur",
        "Sulu",
        "Tawi-Tawi"
    ]
}

def update_municipalities(event):
    selected_region = region_combobox.get()
    municipalities = provinces_in_philippines[selected_region]
    municipality_combobox['values'] = municipalities
    municipality_combobox.set('')

def selected_reg_muni():
    selected_municipality = municipality_combobox.get()

    def update_weather():

            timezone, last_observed, wind_speed, temp, temp_feelslike, cloud_cvrg, precipitation,curr_weather = current_weather_req(selected_municipality,'PH')

            label2.config(text=f"""Timezone: {timezone}
Last Observed: {last_observed}
Current Wind Speed: {wind_speed} m/s
Temperature: {temp} °C
Temp. Feels like: {temp_feelslike} °C
Cloud Coverage: {cloud_cvrg} %
Precipitation: {precipitation} mm/hr
Description: {curr_weather}""")
            
    update_weather()


def click():
    print('You clicked a button')
    pass

def open_website_api():
    url = 'https://www.weatherbit.io/'
    webbrowser.open(url)

window = Tk()

original_image = Image.open('.\\images\\weather-icon.png')
resized_img = original_image.resize((150,110))
icon2 = ImageTk.PhotoImage(resized_img)

window.geometry('440x420')
window.title("Ram's Weather App")
icon = PhotoImage(file='logo.png')
window.iconphoto(True,icon)
window.config(background='lightblue')
window.resizable(False,False)

menubar = Menu(window)
window.config(menu=menubar)

credits = Menu(menubar,tearoff=0)
menubar.add_cascade(label='API',menu=credits)
credits.add_command(label='Weatherbit API',command=open_website_api)

label = Label(window, 
              text="Ram's Forecast",
              bg='#83d4f0', 
              font=('Arial',20,'bold'), 
              fg='white', 
              relief=RAISED,
              bd=5,
              padx=47,
              pady=20,
              image=icon2,
              compound='top')
label.place(x=67,y=25)

label2 = Label(window, 
               text="", 
               width=33, 
               height=8, 
               anchor=tk.W, 
               justify=tk.LEFT,
               wraplength=300,
               relief=SUNKEN)
label2.place(x=180,y=260)

button1 = Button(window, 
                 text='Confirm',
                 command=selected_reg_muni)

button1.place(x=60,y=370)

region_label = ttk.Label(window, text="Select Region:", background='lightblue')
region_label.place(x=50,y=260)

region_combobox = ttk.Combobox(window, values=list(provinces_in_philippines.keys()))
region_combobox.place(x=20,y=285)
region_combobox.bind("<<ComboboxSelected>>", update_municipalities)

municipality_label = ttk.Label(window, text="Select Municipality:", background='lightblue')
municipality_label.place(x=35,y=315)

municipality_combobox = ttk.Combobox(window)
municipality_combobox.place(x=20,y=340)

window.mainloop()