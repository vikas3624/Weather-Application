import requests
from django.shortcuts import render

def weather_view(request):
    error_message = None  # Variable to store error messages
    weather_data = None   # Variable to store weather data if available

    if request.method == 'POST':
        city = request.POST.get('city')  # Get the city name from the form

        if not city:
            error_message = "Please enter a city name."
        else:
            api_key = 'e170d009584f0e24d0fdbaa2b4b1d454'
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}'

            try:
                response = requests.get(url)
                response.raise_for_status()  # Raises an error for non-200 status codes
                weather_data = response.json()

                if weather_data.get('cod') != 200:
                    error_message = f"City '{city}' not found. Please try again."
                else:
                    context = {
                        'city': city,
                        'temperature': weather_data['main']['temp'],
                        'description': weather_data['weather'][0]['description'],
                        'icon': weather_data['weather'][0]['icon'],
                    }
                    return render(request, 'weather.html', context)

            except requests.exceptions.RequestException:
                error_message = "Something went wrong. Please try again later."

    # In case of an error or if no weather data is available, pass the error message to the template
    return render(request, 'weather.html', {'error_message': error_message})
