import requests
import time
from customtkinter import *
from PIL import Image


# define and grid a CTkLabel
def create_label(frame, font, text, height, column, row, column_span, pad_x, pad_y, sticky):
    label = CTkLabel(frame, font=font, text=text, height=height)
    label.grid(column=column, row=row, columnspan=column_span, padx=pad_x, pady=pad_y, sticky=sticky)


# define an image and grid a CTkLabel containing the image
def create_image(frame, path, size, column, row):
    icon = CTkImage(Image.open(path), size=size)
    icon_label = CTkLabel(frame, image=icon, text='')
    icon_label.grid(column=column, row=row)


# unit conversion functions:
def convert_kelvin_to_celsius(temp):
    return temp - 273.15


def convert_kelvin_to_fahrenheit(temp):
    return convert_kelvin_to_celsius(temp) * 1.8 + 32


def convert_mps_to_mph(speed):
    return speed * 2.237


def convert_mps_to_kmh(speed):
    return speed * 3.6


def convert_hpa_to_in(pressure):
    return pressure * 0.02952998


def convert_km_to_mi(distance):
    return distance * 0.621371


class App(CTk):
    def __init__(self):
        super().__init__()

        # API KEY
        self.api_key = "PASTE_YOUR_API_KEY_HERE"
        # fonts
        self.header_font = CTkFont(family='Arial Rounded MT Bold', size=28)
        self.basic_font = CTkFont(family='Arial Rounded MT Bold', size=20)
        self.detail_font = CTkFont(family='Verdana', size=15)
        # settings
        self.temp_units = StringVar(self, 'fahrenheit')
        self.speed_units = StringVar(self, 'mph')
        self.pressure_units = StringVar(self, 'in')
        self.dist_units = StringVar(self, 'mi')
        self.clock = StringVar(self, '12')
        self.theme = StringVar(self, 'system')
        # create variables to store weather data
        self.location_frame = None
        self.location_entry = None
        self.list_frame = None
        self.forecast_frame = None
        self.coordinates = None
        self.location = None
        self.city = None
        self.condition_main = None
        self.condition_description = None
        self.icon = None
        self.temp = None
        self.temp_min = None
        self.temp_max = None
        self.feels_like = None
        self.humidity = None
        self.pressure = None
        self.visibility = None
        self.wind = None
        self.clouds = None
        self.aqi = None
        self.update_time = None
        self.sunrise = None
        self.sunset = None
        self.forecast_data = []
        # GUI
        self.draw_search()

    def draw_search(self):
        # clear screen
        self.clear_frame(self)
        # search screen title
        create_label(self, self.header_font, 'City Search',
                     1, 0, 0, 2, 10, 10, W + E)
        # search bar
        self.location_entry = CTkEntry(self, font=self.basic_font, placeholder_text='Enter city name', width=270)
        self.location_entry.grid(column=0, row=1, padx=(10, 0), pady=10)
        self.location_entry.focus()
        self.location_entry.bind('<Return>', self.get_location)
        search_button = CTkButton(self, text="Go", width=30, command=lambda e: self.get_location(e))
        search_button.grid(column=1, row=1, padx=(0, 10), pady=10)
        # frame containing search results
        self.list_frame = CTkFrame(self, width=300, height=180, border_width=5)
        self.list_frame.grid_propagate(False)
        self.list_frame.grid(column=0, row=2, columnspan=2, padx=10, pady=10)
        # button to go to settings
        settings_button = CTkButton(self, width=300, text='Settings', command=self.draw_settings)
        settings_button.grid(column=0, row=3, columnspan=2, padx=10, pady=10)

    def draw_weather(self):
        # clear screen
        self.clear_frame(self)
        self.clear_frame(self.forecast_frame)

        # top left frame containing location button and description frame
        top_left_frame = CTkFrame(self, fg_color='transparent')
        top_left_frame.grid(column=0, row=0, padx=10, pady=10)
        location_button = CTkButton(top_left_frame, text=self.location, width=300, command=self.draw_search)
        location_button.grid(column=0, row=0)
        create_label(top_left_frame, CTkFont(family='Arial Rounded MT Bold', size=10),
                     f'Last updated: {self.update_time}',
                     10, 0, 1, 1, (9, 0), (11, 1), W)
        # description frame
        description_frame = CTkFrame(top_left_frame, width=300, height=300, border_width=5)
        description_frame.grid_propagate(False)
        description_frame.grid(column=0, row=2)
        create_label(description_frame, self.header_font, self.city,
                     1, 0, 0, 1, 10, (5, 0), W + E)
        create_label(description_frame, CTkFont(family='Arial Rounded MT Bold', size=80), self.temp,
                     1, 0, 1, 1, 10, 0, W + E)
        create_label(description_frame, self.header_font, self.condition_description,
                     1, 0, 2, 1, 10, 0, W + E)
        create_label(description_frame, self.header_font, self.feels_like,
                     1, 0, 3, 1, 10, 0, W + E)
        create_image(description_frame, f'weather_icons/{self.icon}.png', (100, 100), 0, 4)
        description_frame.columnconfigure(0, minsize=300, weight=1)

        # detail frame
        detail_frame = CTkFrame(self, width=400, height=351, border_width=5)
        detail_frame.grid_propagate(False)
        detail_frame.grid(column=1, row=0, padx=10, pady=10)
        create_label(detail_frame, self.header_font, "Today's Weather",
                     1, 0, 0, 4, 10, (5, 0), W + E)
        create_label(detail_frame, self.detail_font, 'Min',
                     1, 0, 1, 1, (10, 0), 0, W)
        create_label(detail_frame, self.detail_font, self.temp_min,
                     1, 1, 1, 1, (0, 10), 0, E)
        create_label(detail_frame, self.detail_font, 'Max',
                     1, 2, 1, 1, (10, 0), 0, W)
        create_label(detail_frame, self.detail_font, self.temp_max,
                     1, 3, 1, 1, (0, 10), 0, E)
        create_label(detail_frame, self.detail_font, 'Humidity',
                     1, 0, 2, 1, (10, 0), 0, W)
        create_label(detail_frame, self.detail_font, self.humidity,
                     1, 1, 2, 1, (0, 10), 0, E)
        create_label(detail_frame, self.detail_font, 'Pressure',
                     1, 2, 2, 1, (10, 0), 0, W)
        create_label(detail_frame, self.detail_font, self.pressure,
                     1, 3, 2, 1, (0, 10), 0, E)
        create_label(detail_frame, self.detail_font, 'Visibility',
                     1, 0, 3, 1, (10, 0), 0, W)
        create_label(detail_frame, self.detail_font, self.visibility,
                     1, 1, 3, 1, (0, 10), 0, E)
        create_label(detail_frame, self.detail_font, 'Clouds',
                     1, 2, 3, 1, (10, 0), 0, W)
        create_label(detail_frame, self.detail_font, self.clouds,
                     1, 3, 3, 1, (0, 10), 0, E)
        create_label(detail_frame, self.detail_font, 'Wind',
                     1, 0, 4, 1, (10, 0), 0, W)
        create_label(detail_frame, self.detail_font, self.wind,
                     1, 1, 4, 1, (0, 10), 0, E)
        create_label(detail_frame, self.detail_font, 'AQI',
                     1, 2, 4, 1, (10, 0), 0, W)
        create_label(detail_frame, self.detail_font, self.aqi,
                     1, 3, 4, 1, (0, 10), 0, E)
        create_label(detail_frame, self.detail_font, 'Sunrise',
                     1, 0, 5, 1, (10, 0), 0, W)
        create_label(detail_frame, self.detail_font, self.sunrise,
                     1, 1, 5, 1, (0, 10), 0, E)
        create_label(detail_frame, self.detail_font, 'Sunset',
                     1, 2, 5, 1, (10, 0), 0, W)
        create_label(detail_frame, self.detail_font, self.sunset,
                     1, 3, 5, 1, (0, 10), 0, E)
        for i in range(4):
            detail_frame.grid_columnconfigure(i, minsize=90, weight=1)
        for i in range(1, 6):
            detail_frame.grid_rowconfigure(i, minsize=70, weight=1)

        # forecast frame
        self.forecast_frame = CTkFrame(self, width=720, height=200, border_width=5)
        self.forecast_frame.grid_propagate(False)
        self.forecast_frame.grid(column=0, row=1, columnspan=2, padx=10, pady=10)
        create_label(self.forecast_frame, self.header_font, "Weather Forecast",
                     1, 0, 0, 5, 10, (5, 25), W + E)
        for i in range(len(self.forecast_data)):
            create_label(self.forecast_frame, self.detail_font, self.forecast_data[i][0],
                         1, i, 1, 1, 0, 0, None)
            create_label(self.forecast_frame, self.detail_font, self.forecast_data[i][1],
                         1, i, 2, 1, 0, 0, None)
            create_image(self.forecast_frame, f'weather_icons/{self.forecast_data[i][2]}.png', (50, 50),
                         i, 3)
            create_label(self.forecast_frame, self.detail_font, self.forecast_data[i][3],
                         1, i, 4, 1, 0, 0, None)
            self.forecast_frame.columnconfigure(i, minsize=144, weight=1)

    def draw_settings(self):
        # clear screen
        self.clear_frame(self)
        # settings screen title
        create_label(self, self.header_font, 'Settings',
                     1, 0, 0, 2, 10, 10, W + E)
        # frame containing all options
        options_frame = CTkFrame(self, width=300, height=300, border_width=5)
        options_frame.grid_propagate(False)
        options_frame.grid(column=0, row=1, padx=10, pady=10)
        create_label(options_frame, self.basic_font, 'Temp:',
                     1, 0, 0, 1, (10, 0), 10, W)
        temp_menu = CTkOptionMenu(options_frame, variable=self.temp_units, values=['fahrenheit', 'celsius'])
        temp_menu.grid(column=1, row=0)
        create_label(options_frame, self.basic_font, 'Speed:',
                     1, 0, 1, 1, (10, 0), 10, W)
        speed_menu = CTkOptionMenu(options_frame, variable=self.speed_units, values=['mph', 'kmh'])
        speed_menu.grid(column=1, row=1)
        create_label(options_frame, self.basic_font, 'Pressure:',
                     1, 0, 2, 1, (10, 0), 10, W)
        pressure_menu = CTkOptionMenu(options_frame, variable=self.pressure_units, values=['in', 'mb'])
        pressure_menu.grid(column=1, row=2)
        create_label(options_frame, self.basic_font, 'Distance:',
                     1, 0, 3, 1, (10, 0), 10, W)
        distance_menu = CTkOptionMenu(options_frame, variable=self.dist_units, values=['mi', 'km'])
        distance_menu.grid(column=1, row=3)
        create_label(options_frame, self.basic_font, 'Clock:',
                     1, 0, 4, 1, (10, 0), 10, W)
        clock_menu = CTkOptionMenu(options_frame, variable=self.clock, values=['12', '24'])
        clock_menu.grid(column=1, row=4)
        create_label(options_frame, self.basic_font, 'Theme:',
                     1, 0, 5, 1, (10, 0), 10, W)
        theme_menu = CTkOptionMenu(options_frame, variable=self.theme, values=['system', 'light', 'dark'],
                                   command=lambda e: self.change_theme(e))
        theme_menu.grid(column=1, row=5)
        for i in range(2):
            options_frame.grid_columnconfigure(i, minsize=150, weight=1)
        for i in range(6):
            options_frame.grid_rowconfigure(i, minsize=20, weight=1)
        # button to return to search screen
        return_button = CTkButton(self, text='Return', command=self.draw_search)
        return_button.grid(column=0, row=2, padx=10, pady=10)

    def get_location(self, event):
        # clear location list frame
        self.clear_frame(self.list_frame)
        # obtain location data
        city = self.location_entry.get()
        url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={self.api_key}'
        location_data = requests.get(url).json()
        num_of_locations = len(location_data)
        locations = []
        for i in range(num_of_locations):
            option = [location_data[i]['name'], [location_data[i]['lat'], location_data[i]['lon']]]
            if 'state' in location_data[i]:
                option[0] += f", {location_data[i]['state']}"
            option[0] += f", {location_data[i]['country']}"
            locations.append(option)
        # create location buttons in location list frame
        for i in range(num_of_locations):
            location_button = CTkButton(self.list_frame, width=290, height=30, corner_radius=0,
                                        text=locations[i][0],
                                        command=lambda j=i: self.get_weather(locations[j], 'e'))
            location_button.grid(column=0, row=i, columnspan=2, padx=5, pady=(5, 0))

    def get_weather(self, location, event):
        self.coordinates = location[1]
        # access api
        url_1 = (f"https://api.openweathermap.org/data/2.5/weather?"
                 f"lat={self.coordinates[0]}&lon={self.coordinates[1]}&appid={self.api_key}")
        weather_data = requests.get(url_1).json()
        url_2 = (f"http://api.openweathermap.org/data/2.5/air_pollution?"
                 f"lat={self.coordinates[0]}&lon={self.coordinates[1]}&appid={self.api_key}")
        aqi_data = requests.get(url_2).json()
        url_3 = (f"http://api.openweathermap.org/data/2.5/forecast?"
                 f"lat={self.coordinates[0]}&lon={self.coordinates[1]}&appid={self.api_key}&cnt=5")
        full_forecast_data = requests.get(url_3).json()

        # obtain general weather data
        self.location = location[0]
        self.city = weather_data['name']
        self.condition_main = weather_data['weather'][0]['main']
        self.condition_description = weather_data['weather'][0]['description'].title()
        self.icon = weather_data['weather'][0]['icon']
        self.humidity = str(weather_data['main']['humidity']) + '%'
        self.clouds = str(weather_data['clouds']['all']) + '%'

        # obtain temperature data based on settings
        match self.temp_units.get():
            case 'fahrenheit':
                self.temp = (str(round(convert_kelvin_to_fahrenheit(weather_data['main']['temp'])))
                             + u'\N{DEGREE SIGN}')
                self.temp_min = (str(round(convert_kelvin_to_fahrenheit(weather_data['main']['temp_min'])))
                                 + u'\N{DEGREE SIGN}')
                self.temp_max = (str(round(convert_kelvin_to_fahrenheit(weather_data['main']['temp_max'])))
                                 + u'\N{DEGREE SIGN}')
                self.feels_like = ('Feels like ' +
                                   (str(round(convert_kelvin_to_fahrenheit(weather_data['main']['feels_like'])))
                                    + u'\N{DEGREE SIGN}'))
            case 'celsius':
                self.temp = (str(round(convert_kelvin_to_celsius(weather_data['main']['temp'])))
                             + u'\N{DEGREE SIGN}')
                self.temp_min = (str(round(convert_kelvin_to_celsius(weather_data['main']['temp_min'])))
                                 + u'\N{DEGREE SIGN}')
                self.temp_max = (str(round(convert_kelvin_to_celsius(weather_data['main']['temp_max'])))
                                 + u'\N{DEGREE SIGN}')
                self.feels_like = ('Feels like ' +
                                   (str(round(convert_kelvin_to_celsius(weather_data['main']['feels_like'])))
                                    + u'\N{DEGREE SIGN}'))

        # obtain pressure data based on settings
        match self.pressure_units.get():
            case 'in':
                self.pressure = str(round(convert_hpa_to_in(weather_data['main']['pressure']), 2)) + ' in'
            case 'mb':
                self.pressure = str(weather_data['main']['pressure']) + ' mb'

        # obtain visibility data based on settings
        match self.dist_units.get():
            case 'mi':
                self.visibility = str(round(convert_km_to_mi(weather_data['visibility'] / 1000), 2)) + ' mi'
            case 'km':
                self.visibility = str(round(weather_data['visibility'] / 1000, 2)) + ' km'

        # obtain wind data
        wind_speed = None
        match self.speed_units.get():
            case 'mph':
                wind_speed = str(round(convert_mps_to_mph(weather_data['wind']['speed']))) + ' mph'
            case 'kmh':
                wind_speed = str(round(convert_mps_to_kmh(weather_data['wind']['speed']))) + ' kmh'
        wind_degree = weather_data['wind']['deg']
        if 0 <= wind_degree < 12 or 349 < wind_degree <= 360:
            wind_direction = 'N'
        elif wind_degree < 34:
            wind_direction = 'NNE'
        elif wind_degree < 57:
            wind_direction = 'NE'
        elif wind_degree < 79:
            wind_direction = 'ENE'
        elif wind_degree < 102:
            wind_direction = 'E'
        elif wind_degree < 124:
            wind_direction = 'ESE'
        elif wind_degree < 147:
            wind_direction = 'SE'
        elif wind_degree < 169:
            wind_direction = 'SSE'
        elif wind_degree < 192:
            wind_direction = 'S'
        elif wind_degree < 214:
            wind_direction = 'SSW'
        elif wind_degree < 237:
            wind_direction = 'SW'
        elif wind_degree < 259:
            wind_direction = 'WSW'
        elif wind_degree < 282:
            wind_direction = 'W'
        elif wind_degree < 304:
            wind_direction = 'WNW'
        elif wind_degree < 327:
            wind_direction = 'NW'
        else:
            wind_direction = 'NNW'
        self.wind = f'{wind_direction} {wind_speed}'

        # obtain sunrise, sunset, and update time data based on settings
        match self.clock.get():
            case '12':
                self.sunrise = time.strftime('%I:%M %p',
                                             time.gmtime(weather_data['sys']['sunrise'] + weather_data['timezone']))
                self.sunset = time.strftime('%I:%M %p',
                                            time.gmtime(weather_data['sys']['sunset'] + weather_data['timezone']))
                self.update_time = time.strftime('%I:%M:%S %p UTC',
                                                 time.gmtime(weather_data['dt']))
            case '24':
                self.sunrise = time.strftime('%H:%M',
                                             time.gmtime(weather_data['sys']['sunrise'] + weather_data['timezone']))
                self.sunset = time.strftime('%H:%M',
                                            time.gmtime(weather_data['sys']['sunset'] + weather_data['timezone']))
                self.update_time = time.strftime('%H:%M:%S UTC',
                                                 time.gmtime(weather_data['dt']))

        # obtain air quality data
        air_quality = aqi_data['list'][0]['main']['aqi']
        match air_quality:
            case 1:
                self.aqi = 'Good'
            case 2:
                self.aqi = 'Fair'
            case 3:
                self.aqi = 'Moderate'
            case 4:
                self.aqi = 'Poor'
            case 5:
                self.aqi = 'Very Poor'

        # obtain weather forecast data
        self.forecast_data = []
        for i in range(full_forecast_data['cnt']):
            forecast_time = full_forecast_data['list'][i]['dt']
            match self.clock.get():
                case '12':
                    forecast_time = time.strftime('%I %p', time.gmtime(forecast_time + weather_data['timezone']))
                case '24':
                    forecast_time = time.strftime('%H:%M', time.gmtime(forecast_time + weather_data['timezone']))
            forecast_temp = full_forecast_data['list'][i]['main']['temp']
            match self.temp_units.get():
                case 'fahrenheit':
                    forecast_temp = (str(round(convert_kelvin_to_fahrenheit(forecast_temp))) + u'\N{DEGREE SIGN}')
                case 'celsius':
                    forecast_time = (str(round(convert_kelvin_to_celsius(forecast_temp))) + u'\N{DEGREE SIGN}')
            self.forecast_data.append([forecast_time, forecast_temp,
                                       full_forecast_data['list'][i]['weather'][0]['icon'],
                                       str(int(full_forecast_data['list'][i]['pop'] * 100)) + '%'])

        # display the collected weather data
        self.draw_weather()

    # remove everything from the screen/frame
    def clear_frame(self, frame):
        if frame is CTkFrame or frame is self:
            for widget in frame.winfo_children():
                widget.grid_forget()

    # change the color theme of the app
    def change_theme(self, event):
        set_appearance_mode(self.theme.get())


if __name__ == '__main__':
    root = App()
    root.title('Weather')
    root.resizable(FALSE, FALSE)
    root.mainloop()
