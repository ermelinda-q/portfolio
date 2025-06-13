#! /bin/bash
# This script downloads the current weather data for Athenry and saves it with a timestamped filename.

# Print the current date and time to the terminal.
date

# Notify the user that the weather data download is starting.
echo "Downloading weather data."

# Download the weather data using wget and save it to the 'data/weather' directory
# with a filename that includes the current date and time (format: YYYYMMDD_HHMMSS.json).
wget -O data/weather/`date +"%Y%m%d_%H%M%S.json"` https://prodapi.metweb.ie/observations/athenry/today

# Notify the user that the weather data has been downloaded successfully.
echo "Weather data downloaded."

# Print the current date and time again to mark the end of the process.
date