
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
