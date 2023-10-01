"""
script to evaluate mean and standard deviation of calculated "Einflussbilanz" to real BISKO data
procedure:
1) read and store data (ags, eev and thg from sectors total, private residences, business (ghd), industry, transport) from source csv file with "real" data, eg. b_ges
-> csv needs to be placed into /data/comp and only contain relevant data
2) calculate "einflussbilanz" by running generator/calculate for all relevant ags
3) use data that is converted into bisko balance, eg. k_ges and all other sectors
4) calculate delta of all sectors: eg. d_ges = (k_ges-b_ges)/b_ges
5) evaluate whether delta data is normal distributed (nd) by Shapiro wilk test
6) if nd, calculate mean and standard distribution for all sectors
7) visualize/plot mean/std.dev/data, atm quantile-quantile plot, hbar/bar plot and boxplot implemented

further information see link: https://germanzero.sharepoint.com/:w:/r/_layouts/15/Doc.aspx?sourcedoc=%7Bd5f349b5-3220-4a25-9f9c-768d33aa393d%7D&action=edit&wdPid=7cc9790b&cid=098abbaa-7144-4e7a-b9f8-635df1fee52b
"""

from comparisonsector import *
from climatevision.generator import calculate_with_default_inputs, RefData, make_entries
from climatevision.tracing import with_tracing
import sys, os

# read csv file containing bisko data for chosen ags
# definitions
SectorTotal = ComparisonSector("Total")
SectorPrivateResidences = ComparisonSector("PrivateResidences")
SectorBusiness = ComparisonSector("Business")
SectorIndustry = ComparisonSector("Industry")
SectorTransport = ComparisonSector("Transport")
Comparison = Comparison()

Comparison.add_sector(SectorTotal, SectorPrivateResidences, SectorBusiness, SectorIndustry, SectorTransport)

Comparison.read_bisko_data()
# iterate through ags, calculate eb and calculate procentual difference to bisko calculation
for i,ags in enumerate(Comparison.rawdata['ags_sample']):
    result = calculate_with_default_inputs(ags, 2030)
    delta_eev_total = ((float(Comparison.rawdata['data_sample'][i].get("eev_ges")))-result.bisko.total.energy)/result.bisko.total.energy
    delta_eev_priv_residences = (float((Comparison.rawdata['data_sample'][i].get("eev_ph")))-result.bisko.priv_residences.total.energy)/result.bisko.priv_residences.total.energy
    delta_eev_business = (float((Comparison.rawdata['data_sample'][i].get("eev_ghd")))-result.bisko.business.total.energy)/result.bisko.business.total.energy
    delta_eev_industry = (float((Comparison.rawdata['data_sample'][i].get("eev_i")))-result.bisko.industry.total.energy)/result.bisko.industry.total.energy
    delta_eev_transport = (float((Comparison.rawdata['data_sample'][i].get("eev_v")))-result.bisko.transport.total.energy)/result.bisko.transport.total.energy
    print("%s/%s" % (i,len(Comparison.rawdata['ags_sample'])))
    Comparison.df_comparison[0].deltas.append(delta_eev_total)
    Comparison.df_comparison[1].deltas.append(delta_eev_priv_residences)
    Comparison.df_comparison[2].deltas.append(delta_eev_business)
    Comparison.df_comparison[3].deltas.append(delta_eev_industry)
    Comparison.df_comparison[4].deltas.append(delta_eev_transport)
    if delta_eev_total > 2:
        print('bisko balance of %s(ags: %s) does not correlate with calculated ev' % (Comparison.rawdata['data_sample'][i].get("name"),Comparison.rawdata['data_sample'][i].get("ags")))

# Check whether datasets pass test for normal distribution
norm_distr_passed = Comparison.shapiro_wilk(0.05, Comparison.df_comparison[0].deltas, Comparison.df_comparison[1].deltas, Comparison.df_comparison[2].deltas, Comparison.df_comparison[3].deltas, Comparison.df_comparison[4].deltas)

if norm_distr_passed: 
    for sector in Comparison.df_comparison:
        sector.avg_deltas()
        sector.std_dev_deltas()
    print('the deviation of the calculated Einflussbilanz to Bisko is approximately following:')
    print('eev total: %.2f(mean), %.2f(standard deviation)' % (Comparison.df_comparison[0].avg, Comparison.df_comparison[0].std_dev))
    print('eev private residences: %.2f(mean), %.2f(standard deviation)' % (Comparison.df_comparison[1].avg, Comparison.df_comparison[1].std_dev))
    print('eev business: %.2f(mean), %.2f(standard deviation)' % (Comparison.df_comparison[2].avg, Comparison.df_comparison[2].std_dev))
    print('eev industry: %.2f(mean), %.2f(standard deviation)' % ( Comparison.df_comparison[3].avg, Comparison.df_comparison[3].std_dev))
    print('eev transport: %.2f(mean), %.2f(standard deviation)' % (Comparison.df_comparison[4].avg, Comparison.df_comparison[4].std_dev))
    Comparison.output()
    Comparison.visualize()
else:
    print('data has no standard distribution. No deviation calculation possible')  

