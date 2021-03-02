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

// creating tables of the regressions we just ran
est table A*, star b(%9.0fc)
