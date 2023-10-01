
Comparison
=========================

TODO list comparison
------------------------
- evaluate final energy consumption (EEV) differences
- continue energy ghg-emission differences
- possibly add KE (see below)

Preparations
------------------------
Please put edited *csv file (reduced to name,ags, eev_ges, eev_ph, eev_ghd, eev_i, eev_v, eev_ke, thg_ges, thg_ph, thg_ghd, thg_i, thg_v, thg_ke)
into path /data/comparison and be sure to adapt name either in script or of file itself.

Abouts
------------------------
This program evaluates the qualitative error of the calculation taking part by the localzero generator.
The evaluation is calculating the average error and standard deviation and is separated by the calculated sectors.
Therefore, BISKO data sets of selected municipalities are compared with the calculated data of the localzero generator.
The selected municipalities are display in dark green within this origin xlsx-file: https://germanzero.sharepoint.com/:x:/r/_layouts/15/Doc.aspx?sourcedoc=%7BD1CF175E-0CB8-40AE-A427-461FE3125F9A%7D&file=22-05-27_Kommunen_BISKO_2018.xlsx&action=default&mobileredirect=true
A reduced table in *csv* is used in order to reduce data amount. 
In order to guarantee comparability of the data sets, the calculated data is converted into BISKO. Furthermore, the data samples are
tested for standard distribution.  
Primarily, the first calculation is only calculating the errors of sectors 	
- Total
- Private households (PH)
- Business (GHD)
- Industry
- Transport 
- Municipal facilities (KE) -> taken out of considerations at first due to expected deviations

Major steps are:
- select data sets (evaluate csv)
- calculate climate vision for cities contained in csv
- convert climate vision data to Bisko
- calculate procentaged difference ((kv-bisko)/bisko) -> first final energy consumption, later ghg
- test for normal distribution -> probably shapiro wilk test 
- calculation of sectorized mean value and standard deviation
- print deviation per sector
