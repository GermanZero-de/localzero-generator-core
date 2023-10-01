"""
functions for comparison of bisko balance 
further information on the methodology see comparison.py
"""

import csv
import json
import matplotlib.pyplot as plt
import scipy.stats as stats

class ComparisonSector:
    def __init__(self, name):
        self.name = name
        self.deltas = []
        self.avg = 0
        self.std_dev = 0
    
    # calculate deltas
    def avg_deltas(self):
        if len(self.deltas)>0:
            self.avg = sum(self.deltas) / len(self.deltas)
        else: 
            self.avg = 0

    # calculate standard deviation
    def std_dev_deltas(self):
        sum = 0
        self.avg_deltas()
        for entry in self.deltas:
            sum += (entry-self.avg)**2
        self.std_dev = (sum/len(self.deltas))**(1/2)

class Comparison:
    def __init__(self):
        self.df_comparison = []
        self.rawdata = {'ags_sample':[], 'data_sample': []}

    def add_sector(self, *sectors:ComparisonSector):
        for sector in sectors:
            self.df_comparison.append(sector)

    def read_bisko_data(self, path="data\\public\\comp\\230525_Kommunen_BISKO_2018_data.csv"):
        with open(path, newline="") as csvfile:
            cityreader = csv.reader(csvfile, delimiter=";")
            next(cityreader)
            for i,row in enumerate(cityreader):
                comp_dict = dict(name=row[0],ags=row[1],eev_ges=row[2],eev_ph=row[3],
                eev_ghd=row[4],eev_i=row[5],eev_v=row[6],eev_ke=row[7],thg_ges=row[8],
                thg_ph=row[9],thg_ghd=row[10],thg_i=row[11],thg_v=row[12],thg_ke=row[13])
                self.rawdata['data_sample'].append(comp_dict)
                self.rawdata['ags_sample'].append(row[1])

    def shapiro_wilk(self, p_target:float, *dataset: list) -> bool:
            if dataset != None:
                passed = True
            else:
                passed = False
                assert("Error! No dataset given")
            for data in dataset:
                statics, p = stats.shapiro(data)
                if p < p_target:
                    print('%s has no standard distribution; p = %s' % ((data), p))
                    passed = False
            return passed
    
    def visualize(self):
        # quantile-quantile plot of deltas to normal distribution
        fig_qq, axs_qq = plt.subplots(nrows=1, ncols=5)
        for i in range(0,len(self.df_comparison)):
           stats.probplot(self.df_comparison[i].deltas, plot=axs_qq[i])
        axs_qq[0].set_title("delta_eev_total")
        axs_qq[1].set_title("delta_priv_res_total")
        axs_qq[2].set_title("delta_eev_business")
        axs_qq[3].set_title("delta_priv_industry")
        axs_qq[4].set_title("delta_eev_transport")

        # configure axis for different plots
        sectors_labels = ["Gesamt","Priv. Haushalte","GHD","Industrie","Verkehr"]
        sectors_axis = [*range(0,len(sectors_labels))]
        data = (self.df_comparison[0].deltas,self.df_comparison[1].deltas,self.df_comparison[2].deltas,self.df_comparison[3].deltas,self.df_comparison[4].deltas)
        means = [self.df_comparison[i].avg for i in range(0, len(sectors_labels))]
        std_devs = [self.df_comparison[i].std_dev for i in range(0, len(sectors_labels))]
        
        # hbar plot with means and standard deviations of all sectors
        fig_hbar, axs_hbar = plt.subplots()
        hbars = axs_hbar.barh(y = sectors_axis, width = means, xerr = std_devs, align="center", )
        axs_hbar.set_title("Fehlerauswertung der Klimavision nach Sektoren")
        axs_hbar.set_xlabel("Durchschnitt (Balken), Standardabweichung (Strich)")
        axs_hbar.set_yticks(sectors_axis, labels=sectors_labels)
        axs_hbar.invert_yaxis()
        axs_hbar.bar_label(hbars, fmt="%.2f")
        axs_hbar.set_xlim(left=-1,right=1.2)
        axs_hbar.xaxis.grid()
    
        # box plot with means 
        fig_box, axs_box = plt.subplots()
        axs_box.boxplot(x=data, positions=[2,4,6,8,10], widths=1.5, labels = sectors_labels)
        axs_box.yaxis.grid()
        axs_box.set_title("Fehlerauswertung der Klimavision nach Sektoren")
        
        #save or show figures
        fig_qq.savefig("comparison\\evaluation\\comparison_qqplot.png")
        fig_hbar.savefig("comparison\\evaluation\\comparison_boxplot.png")
        fig_box.savefig("comparison\\evaluation\\comparisonboxplot.png")
        #plt.show()
    
    def output(self):
        filename = "comparison\\evaluation\\comparison.csv"
        with open(filename,"w",newline="") as file:
            writer = csv.writer(file)
            writer.writerow(self.rawdata['ags_sample'])
            for obj in self.df_comparison:
                writer.writerow(obj.name)
                writer.writerow(obj.deltas)
                writer.writerow([obj.avg])
                writer.writerow([obj.std_dev])
