import numpy as np
import pylab as pl
import csv
pl.ion()

###load data

###USA
us_data=[]
with open('world_dev_indicators_USA/usa_data_2016-07-30.csv') as f:
    reader=csv.reader(f)
    for line in reader:
        us_data.append(line)
        

header0=us_data[0]
header1=us_data[1]
header2=us_data[2]
header3=us_data[3]

header=us_data[4]
us_data=us_data[5:]

###GERMANY
ger_data=[]
with open('world_dev_indicators_GER/germany_data_2016-07-30.csv') as f:
    reader=csv.reader(f)
    for line in reader:
        ger_data.append(line)

header0=ger_data[0]
header1=ger_data[1]
header2=ger_data[2]
header3=ger_data[3]

header=ger_data[4]
ger_data=ger_data[5:]

###BRAZIL
bra_data=[]
with open('world_dev_indicators_BRA/brazil_data_2016-07-30.csv') as f:
    reader=csv.reader(f)
    for line in reader:
        bra_data.append(line)

header=bra_data[4]
bra_data=bra_data[5:]


#sanity check: #check if all indicator names the same in each row
for i,row in enumerate(us_data):
    if row[2]!=ger_data[i][2] or row[3]!=ger_data[i][3]:
        print i, row
for i,row in enumerate(us_data):
    if row[2]!=bra_data[i][2] or row[3]!=bra_data[i][3]:
        print i, row



#sanity check:#check if each row has the same number of columns
num_cols=len(header)
for row in us_data:
    if len(row)!=num_cols:
        print row

###clean up data a little bit. turn numbers into floats, normalize them by raneg and average values

#USA
float_data_us=[]
averages_us=[]
norm_data_us=[]
indicator_list_us=[]

for row in us_data:
    float_row=[float(num) if num!='' else 0.0 for num in row[4:-1]]
    indicator_list_us.append(row[2:4])
    non_zeros=[num for num in float_row if num !=0]
    float_data_us.append(float_row)
    if len(non_zeros)>0:
        average=np.mean(non_zeros)
        list_max=max(non_zeros)
        list_min=min(non_zeros)
        list_range=list_max-list_min
    else:
        average=0
        list_range=1
    if list_range==0:
        list_range=1
    averages_us.append(average)
    norm_row=[(num-average)/list_range if num!=0 else 0.0 for num in float_row]
    norm_data_us.append(norm_row)


#GERMANY
float_data_ger=[]
averages_ger=[]
norm_data_ger=[]
indicator_list_ger=[]

for row in ger_data:
    float_row=[float(num) if num!='' else 0.0 for num in row[4:-1]]
    indicator_list_ger.append(row[2:4])
    non_zeros=[num for num in float_row if num !=0]
    float_data_ger.append(float_row)
    if len(non_zeros)>0:
        average=np.mean(non_zeros)
        list_max=max(non_zeros)
        list_min=min(non_zeros)
        list_range=list_max-list_min
    else:
        average=0
        list_range=1
    if list_range==0:
        list_range=1
    averages_ger.append(average)
    norm_row=[(num-average)/list_range if num!=0 else 0.0 for num in float_row]
    norm_data_ger.append(norm_row)


#BRAZIL
float_data_bra=[]
averages_bra=[]
norm_data_bra=[]
indicator_list_bra=[]

for row in bra_data:
    float_row=[float(num) if num!='' else 0.0 for num in row[4:-1]]
    indicator_list_bra.append(row[2:4])
    non_zeros=[num for num in float_row if num !=0]
    float_data_bra.append(float_row)
    if len(non_zeros)>0:
        average=np.mean(non_zeros)
        list_max=max(non_zeros)
        list_min=min(non_zeros)
        list_range=list_max-list_min
    else:
        average=0
        list_range=1
    if list_range==0:
        list_range=1
    averages_bra.append(average)
    norm_row=[(num-average)/list_range if num!=0 else 0.0 for num in float_row]
    norm_data_bra.append(norm_row)



float_ray_us=np.array(float_data_us)
float_ray_ger=np.array(float_data_ger)
float_ray_bra=np.array(float_data_bra)

norm_ray_us=np.array(norm_data_us)
norm_ray_ger=np.array(norm_data_ger)
norm_ray_bra=np.array(norm_data_bra)

#get rid of indicators taht are zero across the board for all three countries
non_zero_norm_us=[]
non_zero_norm_ger=[]
non_zero_norm_bra=[]
for i,row in enumerate(norm_ray_us):
    ger_row=norm_ray_ger[i]
    bra_row=norm_ray_bra[i]
    if np.sum(row)!=0.0 and np.sum(ger_row)!=0.0 and np.sum(bra_row)!=0: #not sure if requiring all three is the best, might only require two for each pair of countries...
        non_zero_norm_us.append(list(row))
        non_zero_norm_ger.append(list(ger_row))
        non_zero_norm_bra.append(list(bra_row))

non_zero_norm_us=np.array(non_zero_norm_us)
non_zero_norm_ger=np.array(non_zero_norm_ger)
non_zero_norm_bra=np.array(non_zero_norm_bra)

#plot a few indicators for USA
for indicator in norm_ray_us[:10]:
    pl.plot(indicator)

#correlation plots:
## pl.figure()
## for i in range(10):
##     pl.plot(norm_data_us[0],norm_data_us[i],'.')
## pl.axis((0.7,1.3,0.7,1.3))

#correlation plots between ger and US
#each dot in these plots represents the the normalized difference of an indicator from the average of that indicator over all years. A dot alone the linear regression line would mean that that indicator in that year is displaced from that indicators average by a similar amount for both countries

from scipy.stats import linregress
pl.figure()
for i in range(10):
    pl.plot(norm_data_us[i],norm_data_ger[i],'o')
    #slope, intercept, r_value, p_value, std_err = linregress(norm_data_us[i],norm_data_ger[i])
    #pl.plot(norm_data_us[i],np.array(norm_data_us[i])*slope+intercept)
#pl.axis((0.7,1.3,0.7,1.3))

    
#plot each indicator against each other for Ger and US by year

### for usa vs ger
pairs_by_year_usa_ger=np.array([non_zero_norm_us,non_zero_norm_ger]).T
non_zero_pairs_usa_ger=[]
for year in pairs_by_year_usa_ger:
    pairs = [pair for pair in year if (pair[0]!=0 and pair[1]!=0)]
    non_zero_pairs_usa_ger.append(np.array(pairs))

f, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)) = pl.subplots(3, 3)
pl.title('USA vs. GER')

#1970
ax1.plot(non_zero_pairs_usa_ger[10][:,0],non_zero_pairs_usa_ger[10][:,1],'o',color='#0000FF')
slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs_usa_ger[10][:,0],non_zero_pairs_usa_ger[10][:,1])
ax1.plot(range(-1,2),np.array(range(-1,2))*slope+intercept,color='#0000FF')
ax1.set_xlim([-1, 1])
ax1.set_ylim([-1, 1])
ax1.set_title('1970')
#1975
ax2.plot(non_zero_pairs_usa_ger[15][:,0],non_zero_pairs_usa_ger[15][:,1],'o',color='#4400BB')
slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs_usa_ger[15][:,0],non_zero_pairs_usa_ger[15][:,1])
ax2.plot(range(-1,2),np.array(range(-1,2))*slope+intercept,color='#4400BB')
ax2.set_xlim([-1, 1])
ax2.set_ylim([-1, 1])
ax2.set_title('1975')
#1980
ax3.plot(non_zero_pairs_usa_ger[20][:,0],non_zero_pairs_usa_ger[20][:,1],'o',color='#880099')
slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs_usa_ger[20][:,0],non_zero_pairs_usa_ger[20][:,1])
ax3.plot(range(-1,2),np.array(range(-1,2))*slope+intercept,color='#880099')
ax3.set_xlim([-1, 1])
ax3.set_ylim([-1, 1])
ax3.set_title('1980')
#1985
ax4.plot(non_zero_pairs_usa_ger[25][:,0],non_zero_pairs_usa_ger[25][:,1],'o',color='#BB0044')
slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs_usa_ger[25][:,0],non_zero_pairs_usa_ger[25][:,1])
ax4.plot(range(-1,2),np.array(range(-1,2))*slope+intercept,color='#BB0044')
ax4.set_xlim([-1, 1])
ax4.set_ylim([-1, 1])
ax4.set_title('1985')
#1990
ax5.plot(non_zero_pairs_usa_ger[30][:,0],non_zero_pairs_usa_ger[30][:,1],'o',color='#FF0000')
slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs_usa_ger[30][:,0],non_zero_pairs_usa_ger[30][:,1])
ax5.plot(range(-1,2),np.array(range(-1,2))*slope+intercept,color='#FF0000')
ax5.set_xlim([-1, 1])
ax5.set_ylim([-1, 1])
ax5.set_title('1990')
#1995
ax6.plot(non_zero_pairs_usa_ger[35][:,0],non_zero_pairs_usa_ger[35][:,1],'o',color='#BB4400')
slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs_usa_ger[35][:,0],non_zero_pairs_usa_ger[35][:,1])
ax6.plot(range(-1,2),np.array(range(-1,2))*slope+intercept,color='#BB4400')
ax6.set_xlim([-1, 1])
ax6.set_ylim([-1, 1])
ax6.set_title('1995')
#2000
ax7.plot(non_zero_pairs_usa_ger[40][:,0],non_zero_pairs_usa_ger[40][:,1],'o',color='#998800')
slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs_usa_ger[40][:,0],non_zero_pairs_usa_ger[40][:,1])
ax7.plot(range(-1,2),np.array(range(-1,2))*slope+intercept,color='#998800')
ax7.set_xlim([-1, 1])
ax7.set_ylim([-1, 1])
ax7.set_title('2000')
#2005
ax8.plot(non_zero_pairs_usa_ger[45][:,0],non_zero_pairs_usa_ger[45][:,1],'o',color='#44BB00')
slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs_usa_ger[45][:,0],non_zero_pairs_usa_ger[45][:,1])
ax8.plot(range(-1,2),np.array(range(-1,2))*slope+intercept,color='#44BB00')
ax8.set_xlim([-1, 1])
ax8.set_ylim([-1, 1])
ax8.set_title('2005')
#2010
ax9.plot(non_zero_pairs_usa_ger[50][:,0],non_zero_pairs_usa_ger[50][:,1],'o',color='#00FF00')
slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs_usa_ger[50][:,0],non_zero_pairs_usa_ger[50][:,1])
ax9.plot(range(-1,2),np.array(range(-1,2))*slope+intercept,color='#00FF00')
ax9.set_xlim([-1, 1])
ax9.set_ylim([-1, 1])
ax9.set_title('2010')
f.tight_layout()
pl.savefig('Indicator_correlations_US_vs_Ger_w_linregr.png')


#plot each indicator against each other for Ger and Bra by year
### for bra vs ger
pairs_by_year_bra_ger=np.array([non_zero_norm_bra,non_zero_norm_ger]).T
non_zero_pairs_bra_ger=[]
for year in pairs_by_year_bra_ger:
    pairs = [pair for pair in year if (pair[0]!=0 and pair[1]!=0)]
    non_zero_pairs_bra_ger.append(np.array(pairs))

f, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)) = pl.subplots(3, 3)
pl.title('BRA vs. GER')

#1970
ax1.plot(non_zero_pairs_bra_ger[10][:,0],non_zero_pairs_bra_ger[10][:,1],'o',color='#0000FF')
slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs_bra_ger[10][:,0],non_zero_pairs_bra_ger[10][:,1])
ax1.plot(range(-1,2),np.array(range(-1,2))*slope+intercept,color='#0000FF')
ax1.set_xlim([-1, 1])
ax1.set_ylim([-1, 1])
ax1.set_title('1970')
#1975
ax2.plot(non_zero_pairs_bra_ger[15][:,0],non_zero_pairs_bra_ger[15][:,1],'o',color='#4400BB')
slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs_bra_ger[15][:,0],non_zero_pairs_bra_ger[15][:,1])
ax2.plot(range(-1,2),np.array(range(-1,2))*slope+intercept,color='#4400BB')
ax2.set_xlim([-1, 1])
ax2.set_ylim([-1, 1])
ax2.set_title('1975')
#1980
ax3.plot(non_zero_pairs_bra_ger[20][:,0],non_zero_pairs_bra_ger[20][:,1],'o',color='#880099')
slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs_bra_ger[20][:,0],non_zero_pairs_bra_ger[20][:,1])
ax3.plot(range(-1,2),np.array(range(-1,2))*slope+intercept,color='#880099')
ax3.set_xlim([-1, 1])
ax3.set_ylim([-1, 1])
ax3.set_title('1980')
#1985
ax4.plot(non_zero_pairs_bra_ger[25][:,0],non_zero_pairs_bra_ger[25][:,1],'o',color='#BB0044')
slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs_bra_ger[25][:,0],non_zero_pairs_bra_ger[25][:,1])
ax4.plot(range(-1,2),np.array(range(-1,2))*slope+intercept,color='#BB0044')
ax4.set_xlim([-1, 1])
ax4.set_ylim([-1, 1])
ax4.set_title('1985')
#1990
ax5.plot(non_zero_pairs_bra_ger[30][:,0],non_zero_pairs_bra_ger[30][:,1],'o',color='#FF0000')
slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs_bra_ger[30][:,0],non_zero_pairs_bra_ger[30][:,1])
ax5.plot(range(-1,2),np.array(range(-1,2))*slope+intercept,color='#FF0000')
ax5.set_xlim([-1, 1])
ax5.set_ylim([-1, 1])
ax5.set_title('1990')
#1995
ax6.plot(non_zero_pairs_bra_ger[35][:,0],non_zero_pairs_bra_ger[35][:,1],'o',color='#BB4400')
slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs_bra_ger[35][:,0],non_zero_pairs_bra_ger[35][:,1])
ax6.plot(range(-1,2),np.array(range(-1,2))*slope+intercept,color='#BB4400')
ax6.set_xlim([-1, 1])
ax6.set_ylim([-1, 1])
ax6.set_title('1995')
#2000
ax7.plot(non_zero_pairs_bra_ger[40][:,0],non_zero_pairs_bra_ger[40][:,1],'o',color='#998800')
slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs_bra_ger[40][:,0],non_zero_pairs_bra_ger[40][:,1])
ax7.plot(range(-1,2),np.array(range(-1,2))*slope+intercept,color='#998800')
ax7.set_xlim([-1, 1])
ax7.set_ylim([-1, 1])
ax7.set_title('2000')
#2005
ax8.plot(non_zero_pairs_bra_ger[45][:,0],non_zero_pairs_bra_ger[45][:,1],'o',color='#44BB00')
slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs_bra_ger[45][:,0],non_zero_pairs_bra_ger[45][:,1])
ax8.plot(range(-1,2),np.array(range(-1,2))*slope+intercept,color='#44BB00')
ax8.set_xlim([-1, 1])
ax8.set_ylim([-1, 1])
ax8.set_title('2005')
#2010
ax9.plot(non_zero_pairs_bra_ger[50][:,0],non_zero_pairs_bra_ger[50][:,1],'o',color='#00FF00')
slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs_bra_ger[50][:,0],non_zero_pairs_bra_ger[50][:,1])
ax9.plot(range(-1,2),np.array(range(-1,2))*slope+intercept,color='#00FF00')
ax9.set_xlim([-1, 1])
ax9.set_ylim([-1, 1])
ax9.set_title('2010')
f.tight_layout()
pl.savefig('Indicator_correlations_Bra_vs_Ger_w_linregr.png')


#plot each indicator against each other for USA and Bra by year
### for bra vs usa
pairs_by_year_bra_usa=np.array([non_zero_norm_bra,non_zero_norm_us]).T
non_zero_pairs_bra_usa=[]
for year in pairs_by_year_bra_usa:
    pairs = [pair for pair in year if (pair[0]!=0 and pair[1]!=0)]
    non_zero_pairs_bra_usa.append(np.array(pairs))

f, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)) = pl.subplots(3, 3)
pl.title('USA vs. BRA')

#1970
ax1.plot(non_zero_pairs_bra_usa[10][:,0],non_zero_pairs_bra_usa[10][:,1],'o',color='#0000FF')
slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs_bra_usa[10][:,0],non_zero_pairs_bra_usa[10][:,1])
ax1.plot(range(-1,2),np.array(range(-1,2))*slope+intercept,color='#0000FF')
ax1.set_xlim([-1, 1])
ax1.set_ylim([-1, 1])
ax1.set_title('1970')
#1975
ax2.plot(non_zero_pairs_bra_usa[15][:,0],non_zero_pairs_bra_usa[15][:,1],'o',color='#4400BB')
slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs_bra_usa[15][:,0],non_zero_pairs_bra_usa[15][:,1])
ax2.plot(range(-1,2),np.array(range(-1,2))*slope+intercept,color='#4400BB')
ax2.set_xlim([-1, 1])
ax2.set_ylim([-1, 1])
ax2.set_title('1975')
#1980
ax3.plot(non_zero_pairs_bra_usa[20][:,0],non_zero_pairs_bra_usa[20][:,1],'o',color='#880099')
slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs_bra_usa[20][:,0],non_zero_pairs_bra_usa[20][:,1])
ax3.plot(range(-1,2),np.array(range(-1,2))*slope+intercept,color='#880099')
ax3.set_xlim([-1, 1])
ax3.set_ylim([-1, 1])
ax3.set_title('1980')
#1985
ax4.plot(non_zero_pairs_bra_usa[25][:,0],non_zero_pairs_bra_usa[25][:,1],'o',color='#BB0044')
slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs_bra_usa[25][:,0],non_zero_pairs_bra_usa[25][:,1])
ax4.plot(range(-1,2),np.array(range(-1,2))*slope+intercept,color='#BB0044')
ax4.set_xlim([-1, 1])
ax4.set_ylim([-1, 1])
ax4.set_title('1985')
#1990
ax5.plot(non_zero_pairs_bra_usa[30][:,0],non_zero_pairs_bra_usa[30][:,1],'o',color='#FF0000')
slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs_bra_usa[30][:,0],non_zero_pairs_bra_usa[30][:,1])
ax5.plot(range(-1,2),np.array(range(-1,2))*slope+intercept,color='#FF0000')
ax5.set_xlim([-1, 1])
ax5.set_ylim([-1, 1])
ax5.set_title('1990')
#1995
ax6.plot(non_zero_pairs_bra_usa[35][:,0],non_zero_pairs_bra_usa[35][:,1],'o',color='#BB4400')
slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs_bra_usa[35][:,0],non_zero_pairs_bra_usa[35][:,1])
ax6.plot(range(-1,2),np.array(range(-1,2))*slope+intercept,color='#BB4400')
ax6.set_xlim([-1, 1])
ax6.set_ylim([-1, 1])
ax6.set_title('1995')
#2000
ax7.plot(non_zero_pairs_bra_usa[40][:,0],non_zero_pairs_bra_usa[40][:,1],'o',color='#998800')
slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs_bra_usa[40][:,0],non_zero_pairs_bra_usa[40][:,1])
ax7.plot(range(-1,2),np.array(range(-1,2))*slope+intercept,color='#998800')
ax7.set_xlim([-1, 1])
ax7.set_ylim([-1, 1])
ax7.set_title('2000')
#2005
ax8.plot(non_zero_pairs_bra_usa[45][:,0],non_zero_pairs_bra_usa[45][:,1],'o',color='#44BB00')
slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs_bra_usa[45][:,0],non_zero_pairs_bra_usa[45][:,1])
ax8.plot(range(-1,2),np.array(range(-1,2))*slope+intercept,color='#44BB00')
ax8.set_xlim([-1, 1])
ax8.set_ylim([-1, 1])
ax8.set_title('2005')
#2010
ax9.plot(non_zero_pairs_bra_usa[50][:,0],non_zero_pairs_bra_usa[50][:,1],'o',color='#00FF00')
slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs_bra_usa[50][:,0],non_zero_pairs_bra_usa[50][:,1])
ax9.plot(range(-1,2),np.array(range(-1,2))*slope+intercept,color='#00FF00')
ax9.set_xlim([-1, 1])
ax9.set_ylim([-1, 1])
ax9.set_title('2010')
f.tight_layout()
pl.savefig('Indicator_correlations_Bra_vs_USA_w_linregr.png')


#figure out which year has highest correlation coeff

# USA vs GER
yearly_stats_usa_ger=[]
for i in range(len(non_zero_pairs_usa_ger)):
    slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs_usa_ger[i][:,0],non_zero_pairs_usa_ger[i][:,1])
    yearly_stats_usa_ger.append([slope,intercept,r_value,p_value,std_err])
yearly_stats_usa_ger=np.array(yearly_stats_usa_ger)

pl.figure()
year_list=[i+1960 for i in range(len(yearly_stats_usa_ger))]
pl.plot(year_list,yearly_stats_usa_ger[:,2])
pl.title('Correlation coefficient over time')
pl.xlabel('Year')
pl.ylabel('Correlation coefficient')
pl.axvline(x=1990,color='red')#1990, german reunification
pl.text(1991,0.7,'German reunification',color='red')
pl.axis((1960,2020,0.0,0.8))
pl.savefig('Yearly_correlation_coefficients_with_line_USA_GER.png')
#correlation coefficient is how much two variables vary together (covariance) divided by product of their standard deviations:
#R = 1/(n-1)*1/(sig_x*sig_y)*(sum_x_y [(x-mean_x)(y-mean_y)])


# BRA vs GER
yearly_stats_bra_ger=[]
for i in range(len(non_zero_pairs_bra_ger)):
    slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs_bra_ger[i][:,0],non_zero_pairs_bra_ger[i][:,1])
    yearly_stats_bra_ger.append([slope,intercept,r_value,p_value,std_err])
yearly_stats_bra_ger=np.array(yearly_stats_bra_ger)

pl.figure()
year_list=[i+1960 for i in range(len(yearly_stats_bra_ger))]
pl.plot(year_list,yearly_stats_bra_ger[:,2])
pl.title('Correlation coefficient over time')
pl.xlabel('Year')
pl.ylabel('Correlation coefficient')
pl.axvline(x=1990,color='red')#1990, german reunification
pl.text(1991,0.5,'German reunification',color='red')
pl.axis((1960,2020,0.0,0.8))
pl.savefig('Yearly_correlation_coefficients_redline_BRA_GER.png')



# USA vs BRA
yearly_stats_usa_bra=[]
for i in range(len(non_zero_pairs_bra_usa)):
    slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs_bra_usa[i][:,0],non_zero_pairs_bra_usa[i][:,1])
    yearly_stats_usa_bra.append([slope,intercept,r_value,p_value,std_err])
yearly_stats_usa_bra=np.array(yearly_stats_usa_bra)

pl.figure()
year_list=[i+1960 for i in range(len(yearly_stats_usa_bra))]
pl.plot(year_list,yearly_stats_usa_bra[:,2])
pl.title('Correlation coefficient over time')
pl.xlabel('Year')
pl.ylabel('Correlation coefficient')
#pl.axvline(x=1990,color='red')#1990, braman reunification
#pl.text(1991,0.7,'Braman reunification',color='red')
pl.axis((1960,2020,0.0,0.8))
pl.savefig('Yearly_correlation_coefficients_noline_USA_BRA.png')


###all three plots in one figure

pl.figure()
pl.title('Correlation coefficient over time')
pl.xlabel('Year')
pl.ylabel('Correlation coefficient')
pl.plot(year_list,yearly_stats_usa_bra[:,2],label='USA vs. Brazil')
pl.plot(year_list,yearly_stats_usa_ger[:,2],label='USA vs. Germany')
pl.plot(year_list,yearly_stats_bra_ger[:,2],label='Brazil vs. Germany')
pl.legend()
pl.axvline(x=1990,color='red')#1990, german reunification
pl.text(1991,0.5,'German reunification/\nEnd of cold war',color='red')
pl.axis((1960,2020,0.0,0.8))
pl.savefig('Yearly_correlation_coefficients_noline_all_three_pairs_with_line.png')

f, ((ax1, ax2, ax3, ax4)) = pl.subplots(4, 1)
pl.title('Correlation coefficients over time')
nloc = pl.MaxNLocator(3)#max 4 ticks
#usa_ger
ax1.plot(year_list,yearly_stats_usa_ger[:,2],color='red')
#ax1.set_xlim([-, 1])
ax1.set_ylim([0, 0.8])
ax1.axvline(x=1990,color='red')#1990, german reunification
ax1.text(1991,0.5,'German reunification/\nEnd of cold war',color='red')
ax1.set_title('USA vs. GER')
ax1.yaxis.set_major_locator(nloc)

#usa bra
ax2.plot(year_list,yearly_stats_usa_bra[:,2],color='blue')
#ax1.set_xlim([-, 1])
ax2.set_ylim([0, 0.8])
ax2.axvline(x=1990,color='red')#1990, german reunification
ax2.text(1991,0.5,'German reunification/\nEnd of cold war',color='red')
ax2.set_title('USA vs. BRA')
ax2.yaxis.set_major_locator(nloc)

#ger bra
ax3.plot(year_list,yearly_stats_bra_ger[:,2],color='green')
#ax1.set_xlim([-, 1])
ax3.set_ylim([0, 0.8])
ax3.axvline(x=1990,color='red')#1990, german reunification
ax3.text(1991,0.5,'German reunification/\nEnd of cold war',color='red')
ax3.set_title('GER vs. BRA')
ax3.yaxis.set_major_locator(nloc)

#all three
ax4.plot(year_list,yearly_stats_usa_ger[:,2],color='red')
ax4.plot(year_list,yearly_stats_usa_bra[:,2],color='blue')
ax4.plot(year_list,yearly_stats_bra_ger[:,2],color='green')
#ax1.set_xlim([-, 1])
ax4.set_ylim([0, 0.8])
ax4.axvline(x=1990,color='red')#1990, german reunification
ax4.text(1991,0.5,'German reunification/\nEnd of cold war',color='red')
ax4.set_title('USA vs. GER vs. BRA')
ax4.yaxis.set_major_locator(nloc)

f.tight_layout()

pl.savefig('Correlation_coeffs_over_time_grid.png')

## #slope over time
## pl.figure()
## year_list=[i+1960 for i in range(len(yearly_stats))]
## pl.plot(year_list,yearly_stats[:,0])
## pl.plot(year_list,yearly_stats[:,2])
## pl.title('Correlation slope over time')
## pl.xlabel('Year')
## pl.ylabel('Correlation slope')
## #pl.axvline(x=1990,color='red')#1990, german reunification
## #pl.text(1991,0.7,'German reunification',color='red')
## pl.savefig('Yearly_correlation_slope_noline.png')


#figure out which indicator are the most correlated for all years
#for each indicator plot US vs Ger for all years

# USA vs GER
pairs_by_indicator_usa_ger=np.array([norm_ray_us.T,norm_ray_ger.T]).T #indicator X year X 2
non_zero_inds_usa_ger=[]
for ind in pairs_by_indicator_usa_ger:
    pairs = [pair for pair in ind if (pair[0]!=0 and pair[1]!=0)]
    non_zero_inds_usa_ger.append(np.array(pairs))
#creates time series of indicators removing any pairs where any of the indicators is zero

indicator_stats_usa_ger=[]
for i,ind in enumerate(non_zero_inds_usa_ger):
    if len(ind)>20:#linear regression with less points is kind of moot
        slope, intercept, r_value, p_value, std_err = linregress(ind[:,0],ind[:,1])
        indicator_stats_usa_ger.append([slope, intercept, r_value, p_value, std_err])
    else:
        indicator_stats_usa_ger.append([0,0,0,0,0])

indicator_stats_usa_ger=np.array(indicator_stats_usa_ger)

slopes_usa_ger=indicator_stats_usa_ger[:,0]
r_vals_usa_ger=indicator_stats_usa_ger[:,2]
squared_r_usa_ger=r_vals_usa_ger**2 #pairwise square
sorted_squares_usa_ger=np.sort(squared_r_usa_ger)[::-1]
over09_usa_ger=np.argwhere(squared_r_usa_ger>0.9)
sorted_r_usa_ger=np.sort(r_vals_usa_ger)
sort_args_usa_ger=np.argsort(r_vals_usa_ger)[::-1]#highest correlation first

# USA vs BRA
pairs_by_indicator_usa_bra=np.array([norm_ray_us.T,norm_ray_bra.T]).T #indicator X year X 2
non_zero_inds_usa_bra=[]
for ind in pairs_by_indicator_usa_bra:
    pairs = [pair for pair in ind if (pair[0]!=0 and pair[1]!=0)]
    non_zero_inds_usa_bra.append(np.array(pairs))
#creates time series of indicators removing any pairs where any of the indicators is zero

indicator_stats_usa_bra=[]
for i,ind in enumerate(non_zero_inds_usa_bra):
    if len(ind)>20:#linear regression with less points is kind of moot
        slope, intercept, r_value, p_value, std_err = linregress(ind[:,0],ind[:,1])
        indicator_stats_usa_bra.append([slope, intercept, r_value, p_value, std_err])
    else:
        indicator_stats_usa_bra.append([0,0,0,0,0])

indicator_stats_usa_bra=np.array(indicator_stats_usa_bra)

slopes_usa_bra=indicator_stats_usa_bra[:,0]
r_vals_usa_bra=indicator_stats_usa_bra[:,2]
squared_r_usa_bra=r_vals_usa_bra**2 #pairwise square
sorted_squares_usa_bra=np.sort(squared_r_usa_bra)[::-1]
over09_usa_bra=np.argwhere(squared_r_usa_bra>0.9)
sorted_r_usa_bra=np.sort(r_vals_usa_bra)
sort_args_usa_bra=np.argsort(r_vals_usa_bra)[::-1]#highest correlation first


# GER vs BRA
pairs_by_indicator_ger_bra=np.array([norm_ray_us.T,norm_ray_bra.T]).T #indicator X year X 2
non_zero_inds_ger_bra=[]
for ind in pairs_by_indicator_ger_bra:
    pairs = [pair for pair in ind if (pair[0]!=0 and pair[1]!=0)]
    non_zero_inds_ger_bra.append(np.array(pairs))
#creates time series of indicators removing any pairs where any of the indicators is zero

indicator_stats_ger_bra=[]
for i,ind in enumerate(non_zero_inds_ger_bra):
    if len(ind)>20:#linear regression with less points is kind of moot
        slope, intercept, r_value, p_value, std_err = linregress(ind[:,0],ind[:,1])
        indicator_stats_ger_bra.append([slope, intercept, r_value, p_value, std_err])
    else:
        indicator_stats_ger_bra.append([0,0,0,0,0])

indicator_stats_ger_bra=np.array(indicator_stats_ger_bra)

slopes_ger_bra=indicator_stats_ger_bra[:,0]
r_vals_ger_bra=indicator_stats_ger_bra[:,2]
squared_r_ger_bra=r_vals_ger_bra**2 #pairwise square
sorted_squares_ger_bra=np.sort(squared_r_ger_bra)[::-1]
over09_ger_bra=np.argwhere(squared_r_ger_bra>0.9)
sorted_r_ger_bra=np.sort(r_vals_ger_bra)
sort_args_ger_bra=np.argsort(r_vals_ger_bra)[::-1]#highest correlation first


#plot exmple correlation plot (highest correlation)
pl.figure()
indicator_i=sort_args[0]
indicator_name=indicator_list_us[indicator_i]
pl.plot(non_zero_inds[indicator_i][:,0],non_zero_inds[indicator_i][:,1],'.')
slope, intercept, r_value, p_value, std_err = linregress(non_zero_inds[indicator_i][:,0],non_zero_inds[indicator_i][:,1])
pl.plot([-0.5,0.6],np.array([-0.5,0.6])*slope+intercept)
pl.title(indicator_name[0]+' (US vs. GER)')
pl.xlabel('Normalized value (USA)')
pl.ylabel('Normalized value (Germany)')
pl.text(-0.2,0.4,"R = "+str(np.round(r_value,3)),fontsize=20)
pl.savefig('Mortality_rate_correlation_plot.png')

#histogram of r values

non_zero_rvals=[val for val in r_vals if val!=0]
pl.figure()
pl.hist(non_zero_rvals,bins=100)
pl.xlabel('Pairwise Correlation Coefficient')
pl.ylabel('Count')
pl.savefig('Histogram_pairwise_correlation_coefficients.png')

pl.plot(sorted_r)
## print np.argmax(squared_r),np.max(squared_r)

## #print top ten correlated indicators
print np.array(indicator_list_us)[sort_args[:10]]
top10_inds = np.array(indicator_list_us)[sort_args[:10]]

## #print top ten negative correlatoins
print np.array(indicator_list_us)[sort_args[-10:]]
top10_neg = np.array(indicator_list_us)[sort_args[-10:]]

#print top correlation:
pl.figure()
pl.plot(non_zero_inds[sort_args[0]][:,0],non_zero_inds[sort_args[0]][:,1],'.')
#unnormalized data, correlation plot
pl.figure()
pl.plot(np.array(float_data_us)[sort_args[0]],np.array(float_data_ger)[sort_args[0]],'.')

#unnormalized data plot over time
pl.figure()
pl.plot(np.array(float_data_us)[sort_args[0]])
pl.plot(np.array(float_data_ger)[sort_args[0]])

#plot top 4 positive and top 4 negative correlations in unnormalized values
start_year=1960
year_list=np.array(range(56))+start_year

#USA vs GER

f, (topax, bottomax) = pl.subplots(2, 4)
#pl.title('USA vs. GER - correlated indicators over time')
xloc = pl.MaxNLocator(2)#max 3 ticks

#positive correlations
for i in range(4):
    us_nums = np.array(float_data_us)[sort_args_usa_ger[i]]
    us_nan = [num if num!=0 else np.nan for num in us_nums]
    print len(us_nan)
    topax[i].plot(year_list,us_nan,color='blue')
    ger_nums = np.array(float_data_ger)[sort_args_usa_ger[i]]
    ger_nan = [num if num!=0 else np.nan for num in ger_nums]
    print len(ger_nan)
    topax[i].plot(year_list,ger_nan,color='gold')
    short_title=indicator_list_us[sort_args_usa_ger[i]][0][:20]
    print short_title
    topax[i].set_title(short_title,size=10)
    topax[i].xaxis.set_major_locator(xloc)
    topax[i].axvline(x=1990,color='red')#1990, german reunification

#negative correlations
for i in range(4):
    us_nums = np.array(float_data_us)[sort_args_usa_ger[::-1][i]]
    us_nan = [num if num!=0 else np.nan for num in us_nums]
    print len(us_nan)
    bottomax[i].plot(year_list,us_nan,color='blue')
    ger_nums = np.array(float_data_ger)[sort_args_usa_ger[::-1][i]]
    ger_nan = [num if num!=0 else np.nan for num in ger_nums]
    print len(ger_nan)
    bottomax[i].plot(year_list,ger_nan,color='gold')
    short_title=indicator_list_us[sort_args_usa_ger[::-1][i]][0][:20]
    print short_title
    bottomax[i].set_title(short_title,size=10)    
    bottomax[i].xaxis.set_major_locator(xloc)
    bottomax[i].axvline(x=1990,color='red')#1990, german reunification

f.tight_layout()
pl.savefig('Indicator_top_correlations_US_vs_Ger_w_reunification_line.png')

# USA vs BRA

f, (topax, bottomax) = pl.subplots(2, 4)
#pl.title('USA vs. BRA - correlated indicators over time')
xloc = pl.MaxNLocator(2)#max 3 ticks

#positive correlations
for i in range(4):
    us_nums = np.array(float_data_us)[sort_args_usa_bra[i]]
    us_nan = [num if num!=0 else np.nan for num in us_nums]
    print len(us_nan)
    topax[i].plot(year_list,us_nan,color='blue')
    bra_nums = np.array(float_data_bra)[sort_args_usa_bra[i]]
    bra_nan = [num if num!=0 else np.nan for num in bra_nums]
    print len(bra_nan)
    topax[i].plot(year_list,bra_nan,color='gold')
    short_title=indicator_list_us[sort_args_usa_bra[i]][0][:20]
    print short_title
    topax[i].set_title(short_title,size=10)
    topax[i].xaxis.set_major_locator(xloc)
    topax[i].axvline(x=1990,color='red')#1990, braman reunification

#negative correlations
for i in range(4):
    us_nums = np.array(float_data_us)[sort_args_usa_bra[::-1][i]]
    us_nan = [num if num!=0 else np.nan for num in us_nums]
    print len(us_nan)
    bottomax[i].plot(year_list,us_nan,color='blue')
    bra_nums = np.array(float_data_bra)[sort_args_usa_bra[::-1][i]]
    bra_nan = [num if num!=0 else np.nan for num in bra_nums]
    print len(bra_nan)
    bottomax[i].plot(year_list,bra_nan,color='gold')
    short_title=indicator_list_us[sort_args_usa_bra[::-1][i]][0][:20]
    print short_title
    bottomax[i].set_title(short_title,size=10)    
    bottomax[i].xaxis.set_major_locator(xloc)
    bottomax[i].axvline(x=1990,color='red')#1990, braman reunification

f.tight_layout()
pl.savefig('Indicator_top_correlations_US_vs_Bra_w_reunification_line.png')


# GER vs BRA

f, (topax, bottomax) = pl.subplots(2, 4)
#pl.title('GER vs. BRA - correlated indicators over time')
xloc = pl.MaxNLocator(2)#max 3 ticks

#positive correlations
for i in range(4):
    us_nums = np.array(float_data_us)[sort_args_ger_bra[i]]
    us_nan = [num if num!=0 else np.nan for num in us_nums]
    print len(us_nan)
    topax[i].plot(year_list,us_nan,color='blue')
    bra_nums = np.array(float_data_bra)[sort_args_ger_bra[i]]
    bra_nan = [num if num!=0 else np.nan for num in bra_nums]
    print len(bra_nan)
    topax[i].plot(year_list,bra_nan,color='gold')
    short_title=indicator_list_us[sort_args_ger_bra[i]][0][:20]
    print short_title
    topax[i].set_title(short_title,size=10)
    topax[i].xaxis.set_major_locator(xloc)
    topax[i].axvline(x=1990,color='red')#1990, braman reunification

#negative correlations
for i in range(4):
    us_nums = np.array(float_data_us)[sort_args_ger_bra[::-1][i]]
    us_nan = [num if num!=0 else np.nan for num in us_nums]
    print len(us_nan)
    bottomax[i].plot(year_list,us_nan,color='blue')
    bra_nums = np.array(float_data_bra)[sort_args_ger_bra[::-1][i]]
    bra_nan = [num if num!=0 else np.nan for num in bra_nums]
    print len(bra_nan)
    bottomax[i].plot(year_list,bra_nan,color='gold')
    short_title=indicator_list_us[sort_args_ger_bra[::-1][i]][0][:20]
    print short_title
    bottomax[i].set_title(short_title,size=10)    
    bottomax[i].xaxis.set_major_locator(xloc)
    bottomax[i].axvline(x=1990,color='red')#1990, braman reunification

f.tight_layout()
pl.savefig('Indicator_top_correlations_Ger_vs_Bra_w_reunification_line.png')
