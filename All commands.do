// Changing the given divvy data to be able to use in project

use "/Users/nancyli/Desktop/ECON 11020 Final Project/Divvy data by date and origin.dta"

collapse (sum) trips, by(start_date)
gen date_string = string(start_date)
destring date_string, replace
recast float date_string

// creating month and day variables
gen date_temp = string(start_date, "%td")
gen month = substr(date_temp, 3,3)
gen num_month = 0
replace num_month = 1 if month == "jan"
replace num_month = 2 if month == "feb"
replace num_month = 3 if month == "mar"
replace num_month = 4 if month == "apr"
replace num_month = 5 if month == "may"
replace num_month = 6 if month == "jun"
replace num_month = 7 if month == "jul"
replace num_month = 8 if month == "aug"
replace num_month = 9 if month == "sep"
replace num_month = 10 if month == "oct"
replace num_month = 11 if month == "nov"
replace num_month = 12 if month == "dec"

gen day_temp = substr(date_temp, 1,2)
gen day = real(day_temp)
drop day_temp
drop date_temp

// This creates a variables for seasons.
gen summer = 0
replace summer = 1 if month == "jun" | month == "jul" | month == "aug"

gen winter = 0
replace winter = 1 if month == "dec" | month == "jan" | month == "feb"

gen spring = 0
replace spring = 2 if month == "mar" | month == "apr" | month == "may"

gen autumn = 0
replace autumn = 4 if month == "sep" | month == "oct" | month == "nov"

save "DivvyDataEdited.dta", replace


// Cleaning the raw weather data, so that it can be used
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

// merging the two data sets for easy regressions
use "/Users/nancyli/Desktop/ECON 11020 Final Project/cleaned-weather-data.dta"

merge 1:1 date_string using "DivvyDataEdited.dta"
drop _merge
drop start_date
drop new_date
drop new_date1
gen day_of_week = dow(date_string)
gen lntrips = ln(trips)

save "merged_data.dta", replace

// creating graph of trips and average temperature
line trips temp_avg

// running regressions
use "/Users/nancyli/Desktop/ECON 11020 Final Project/merged_data.dta"


// regressing trips against average temperature and controlling for other regressors
regress trips temp_avg
est sto A1

regress trips temp_avg snow_depth
est sto A2

regress trips temp_avg snow_depth snow
est sto A3

regress trips temp_avg snow_depth snow thunder
est sto A4

regress trips temp_avg snow_depth snow thunder prcp
est sto A5

regress trips temp_avg snow_depth snow thunder prcp sleet
est sto A6

regress trips temp_avg snow_depth snow thunder prcp sleet hail
est sto A7

regress trips temp_avg snow_depth snow thunder prcp sleet hail rime
est sto A8

regress trips temp_avg snow_depth snow thunder prcp sleet hail rime smoke
est sto A9

regress trips temp_avg snow_depth snow thunder prcp sleet hail rime smoke wind
est sto A10

regress trips temp_avg snow_depth snow thunder prcp sleet hail rime smoke wind num_month
est sto A11

regress trips temp_avg snow_depth snow thunder prcp sleet hail rime smoke wind num_month day
est sto A12

regress trips temp_avg snow_depth snow thunder prcp sleet hail rime smoke wind num_month day summer
est sto A13

regress trips temp_avg snow_depth snow thunder prcp sleet hail rime smoke wind num_month day summer winter
est sto A14

regress trips temp_avg snow_depth snow thunder prcp sleet hail rime smoke wind num_month day summer winter spring
est sto A15

regress trips temp_avg snow_depth snow thunder prcp sleet hail rime smoke wind num_month day summer winter spring autumn
est sto A16

regress trips temp_avg snow_depth snow thunder prcp sleet hail rime smoke wind num_month day summer winter spring autumn day_of_week
est sto A17

//
regress lntrips temp_avg
est sto B1

regress lntrips temp_avg snow_depth
est sto B2

regress lntrips temp_avg snow_depth snow
est sto B3

regress lntrips temp_avg snow_depth snow thunder
est sto B4

regress lntrips temp_avg snow_depth snow thunder prcp
est sto B5

regress lntrips temp_avg snow_depth snow thunder prcp sleet
est sto B6

regress lntrips temp_avg snow_depth snow thunder prcp sleet hail
est sto B7

regress lntrips temp_avg snow_depth snow thunder prcp sleet hail rime
est sto B8

regress lntrips temp_avg snow_depth snow thunder prcp sleet hail rime smoke
est sto B9

regress lntrips temp_avg snow_depth snow thunder prcp sleet hail rime smoke wind
est sto B10

regress lntrips temp_avg snow_depth snow thunder prcp sleet hail rime smoke wind num_month
est sto B11

regress lntrips temp_avg snow_depth snow thunder prcp sleet hail rime smoke wind num_month day
est sto B12

regress lntrips temp_avg snow_depth snow thunder prcp sleet hail rime smoke wind num_month day summer
est sto B13

regress lntrips temp_avg snow_depth snow thunder prcp sleet hail rime smoke wind num_month day summer winter
est sto B14

regress lntrips temp_avg snow_depth snow thunder prcp sleet hail rime smoke wind num_month day summer winter spring
est sto B15

regress lntrips temp_avg snow_depth snow thunder prcp sleet hail rime smoke wind num_month day summer winter spring autumn
est sto B16

regress lntrips temp_avg snow_depth snow thunder prcp sleet hail rime smoke wind num_month day summer winter spring autumn day_of_week
est sto B17

// creating tables of the regressions we just ran
est table A*, star b(%9.0fc)
est table B*, star b(%9.0fc)
