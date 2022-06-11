# German Teletext Weather View

This python script generates a gif with a weather overview for germany.
The gif is based on old teletext pages restored on <https://www.videotexxxt.org/>.
The `slide*.png` images are used as templates, [Pillow](https://github.com/python-pillow/Pillow) 
is used for image manipulation,[OpenWeather](https://openweathermap.org/api) for
weather data. You will need an (free) api key if you plan on running the tool yourself.

## How to run

0. Clone the repository
1. Edit the `conf.py` file according to your needs, and supply your api key
2. Install the needed python dependencies:


```sh
pip install pillow requests
```

3. Download the EuropeanTeletextNuevo font (e.g. [here](https://www.dafont.com/de/european-teletext.font))
4. Run:

```sh
python Teletext.py
```

## Example output

![Example of the output gif](https://raw.githubusercontent.com/NoahFreising/TeletextWeather/main/wetter.gif)
