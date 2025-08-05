import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pyttsx3

# Voice engine setup
engine = pyttsx3.init()

# Advice based on weather
def get_weather_advice(description):
    desc = description.lower()
    if "rain" in desc or "thunder" in desc or "storm" in desc:
        return "You may want to stay indoors."
    elif "clear" in desc or "sun" in desc:
        return "It's a nice day to go outside."
    elif "cloud" in desc:
        return "It might be a bit cloudy, but it's okay."
    else:
        return "Be prepared for unpredictable weather."

# Function to get weather and update GUI
def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name")
        return

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=5e6a90ac2e9c759194b18e579d8fb396&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            messagebox.showerror("Error", f"City '{city}' not found.")
            return

        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        advice = get_weather_advice(desc)

        # Update labels
        weather_info.config(text=f"{city}\n{temp}°C\n{desc}")
        weather_advice.config(text=advice)

        # Update icon
        icon_name = get_icon_filename(desc)
        try:
            icon = Image.open(f"assets/{icon_name}")
            icon = icon.resize((100, 100))
            icon_image = ImageTk.PhotoImage(icon)
            icon_label.config(image=icon_image)
            icon_label.image = icon_image
        except:
            pass

        # Voice output
        engine.say(f"The current weather in {city} is {desc} and temperature is {temp} degree Celsius. {advice}")
        engine.runAndWait()

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Match weather description to icon filename
def get_icon_filename(description):
    desc = description.lower()
    if "clear" in desc:
        return "sun.png"
    elif "cloud" in desc:
        return "cloud.png"
    elif "rain" in desc:
        return "rain.png"
    elif "thunder" in desc:
        return "thunder.png"
    elif "snow" in desc:
        return "snow.png"
    elif "mist" in desc or "fog" in desc:
        return "mist.png"
    else:
        return "logo.png"

# GUI Setup
root = tk.Tk()
root.title("Weather App")
root.geometry("350x500")
root.resizable(False, False)

# Logo
logo_img = Image.open("assets/logo.png")
logo_img = logo_img.resize((100, 100))
logo_photo = ImageTk.PhotoImage(logo_img)
icon_label = tk.Label(root, image=logo_photo)
icon_label.pack(pady=10)

# Entry box
city_entry = tk.Entry(root, font=("Helvetica", 16), justify="center")
city_entry.pack(pady=10)
city_entry.insert(0, "Enter City Name")

# Button
search_button = tk.Button(root, text="Get Weather", font=("Helvetica", 14), command=get_weather)
search_button.pack(pady=10)

# Weather info
weather_info = tk.Label(root, font=("Helvetica", 16), justify="center")
weather_info.pack(pady=20)

# Advice
weather_advice = tk.Label(root, font=("Helvetica", 12), wraplength=300, fg="green", justify="center")
weather_advice.pack()

# Main loop
root.mainloop()
