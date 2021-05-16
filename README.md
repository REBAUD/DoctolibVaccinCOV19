# DoctolibVaccinCOV19

This script ask to Doctolib the vaccination centers close to "city" variable, and keep only the ones closer than "tolerancy_radius" around "geoloc".
Each 2s, the script will ask to Doctolib if a slot is available, one places by one at each time.
Once a slot is found, a web page is openned, and a bip is emitted.

To adapt to your position, change : 
- **city** : write the city name like villeneuve-saint-georges
- **geoloc** : using the result from here : https://www.gps-longitude-latitude.net/longitude-latitude-coordonnees-gps-du-lieu
- **tolerancy_radius** : Define the tolerancy distance around geoloc position in km.


The folowing packages has to be installed : 
- math
- datetime
- time
- requests
- json
-  re
- winsound
- webbrowser