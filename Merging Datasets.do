// Merging Datasets


use "/Users/nancyli/Desktop/ECON 11020 Final Project/cleaned-weather-data.dta"

merge 1:1 date_string using "DivvyDataEdited.dta"
drop _merge
drop start_date
drop new_date
drop new_date1
gen day_of_week = dow(date_string)
gen lntrips = ln(trips)

save "merged_data.dta", replace


