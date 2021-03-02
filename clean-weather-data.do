// This script cleans the weather data, as the raw data has gaps

use "/Users/nancyli/Desktop/ECON 11020 Final Project/raw_weather_data.dta"


collapse tmax tmin tavg snwd (sum) snow wt03 prcp wt04 wt05 wt06 wt08 wt11, by(date)


// sort table by date
gen new_date = date
gen new_date1 = date(new_date, "MD20Y")
gsort new_date1

// deletes empty rows
drop if date == ""

// renaming variables so that they are more user friendly
rename tmax temp_max
rename tmin temp_min
rename tavg temp_avg
rename snwd snow_depth
rename wt03 thunder
rename wt04 sleet
rename wt05 hail
rename wt06 rime
rename wt08 smoke
rename wt11 wind

// dummy variables: snow thunder prcp sleet hail rime smoke wind
// converting to dummy variables

replace snow = 1 if snow > 0
replace thunder = 1 if thunder > 0
replace prcp = 1 if prcp > 0
replace sleet = 1 if sleet > 0
replace hail = 1 if hail > 0
replace rime = 1 if rime > 0
replace smoke = 1 if smoke > 0
replace wind = 1 if wind > 0

gen date_string = new_date1
format date_string %10.0g

save "cleaned-weather-data.dta", replace
