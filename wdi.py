import numpy as np
import pylab as pl
import csv
pl.ion()

us_data=[]
with open('world_dev_indicators/world_development_indicators_US.csv') as f:
    reader=csv.reader(f)
    for line in reader:
        us_data.append(line)
        

header0=us_data[0]
header1=us_data[1]
header2=us_data[2]
header3=us_data[3]

header=us_data[4]
us_data=us_data[5:]


ger_data=[]
with open('world_dev_indicators_GER/world_dev_indicators_GER.csv') as f:
    reader=csv.reader(f)
    for line in reader:
        ger_data.append(line)

header0=ger_data[0]
header1=ger_data[1]
header2=ger_data[2]
header3=ger_data[3]

header=ger_data[4]
ger_data=ger_data[5:]

#sanity check:
for i,row in enumerate(us_data):
    if row[2]!=ger_data[i][2] or row[3]!=ger_data[i][3]:
        print i, row

#sanity check:
num_cols=len(header)
for row in us_data:
    if len(row)!=num_cols:
        print row

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



float_ray_us=np.array(float_data_us)
float_ray_ger=np.array(float_data_ger)

norm_ray_us=np.array(norm_data_us)
norm_ray_ger=np.array(norm_data_ger)

non_zero_norm_us=[]
non_zero_norm_ger=[]
for i,row in enumerate(norm_ray_us):
    ger_row=norm_ray_ger[i]
    if np.sum(row)!=0.0 and np.sum(ger_row)!=0.0:
        non_zero_norm_us.append(list(row))
        non_zero_norm_ger.append(list(ger_row))

non_zero_norm_us=np.array(non_zero_norm_us)
non_zero_norm_ger=np.array(non_zero_norm_ger)

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
pl.axis((0.7,1.3,0.7,1.3))

pairs_by_year=np.array([non_zero_norm_us,non_zero_norm_ger]).T
non_zero_pairs=[]
for year in pairs_by_year:
    pairs = [pair for pair in year if (pair[0]!=0 and pair[1]!=0)]
    non_zero_pairs.append(np.array(pairs))
    
#plot each indicator against each other for Ger and US by year

f, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)) = pl.subplots(3, 3)
pl.title('USA vs. GER')

#1970
ax1.plot(non_zero_pairs[10][:,0],non_zero_pairs[10][:,1],'o',color='#0000FF')
slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs[10][:,0],non_zero_pairs[10][:,1])
ax1.plot(range(-1,2),np.array(range(-1,2))*slope+intercept,color='#0000FF')
ax1.set_xlim([-1, 1])
ax1.set_ylim([-1, 1])
ax1.set_title('1970')
#1975
ax2.plot(non_zero_pairs[15][:,0],non_zero_pairs[15][:,1],'o',color='#4400BB')
slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs[15][:,0],non_zero_pairs[15][:,1])
ax2.plot(range(-1,2),np.array(range(-1,2))*slope+intercept,color='#4400BB')
ax2.set_xlim([-1, 1])
ax2.set_ylim([-1, 1])
ax2.set_title('1975')
#1980
ax3.plot(non_zero_pairs[20][:,0],non_zero_pairs[20][:,1],'o',color='#880099')
slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs[20][:,0],non_zero_pairs[20][:,1])
ax3.plot(range(-1,2),np.array(range(-1,2))*slope+intercept,color='#880099')
ax3.set_xlim([-1, 1])
ax3.set_ylim([-1, 1])
ax3.set_title('1980')
#1985
ax4.plot(non_zero_pairs[25][:,0],non_zero_pairs[25][:,1],'o',color='#BB0044')
slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs[25][:,0],non_zero_pairs[25][:,1])
ax4.plot(range(-1,2),np.array(range(-1,2))*slope+intercept,color='#BB0044')
ax4.set_xlim([-1, 1])
ax4.set_ylim([-1, 1])
ax4.set_title('1985')
#1990
ax5.plot(non_zero_pairs[30][:,0],non_zero_pairs[30][:,1],'o',color='#FF0000')
slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs[30][:,0],non_zero_pairs[30][:,1])
ax5.plot(range(-1,2),np.array(range(-1,2))*slope+intercept,color='#FF0000')
ax5.set_xlim([-1, 1])
ax5.set_ylim([-1, 1])
ax5.set_title('1990')
#1995
ax6.plot(non_zero_pairs[35][:,0],non_zero_pairs[35][:,1],'o',color='#BB4400')
slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs[35][:,0],non_zero_pairs[35][:,1])
ax6.plot(range(-1,2),np.array(range(-1,2))*slope+intercept,color='#BB4400')
ax6.set_xlim([-1, 1])
ax6.set_ylim([-1, 1])
ax6.set_title('1995')
#2000
ax7.plot(non_zero_pairs[40][:,0],non_zero_pairs[40][:,1],'o',color='#998800')
slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs[40][:,0],non_zero_pairs[40][:,1])
ax7.plot(range(-1,2),np.array(range(-1,2))*slope+intercept,color='#998800')
ax7.set_xlim([-1, 1])
ax7.set_ylim([-1, 1])
ax7.set_title('2000')
#2005
ax8.plot(non_zero_pairs[45][:,0],non_zero_pairs[45][:,1],'o',color='#44BB00')
slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs[45][:,0],non_zero_pairs[45][:,1])
ax8.plot(range(-1,2),np.array(range(-1,2))*slope+intercept,color='#44BB00')
ax8.set_xlim([-1, 1])
ax8.set_ylim([-1, 1])
ax8.set_title('2005')
#2010
ax9.plot(non_zero_pairs[50][:,0],non_zero_pairs[50][:,1],'o',color='#00FF00')
slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs[50][:,0],non_zero_pairs[50][:,1])
ax9.plot(range(-1,2),np.array(range(-1,2))*slope+intercept,color='#00FF00')
ax9.set_xlim([-1, 1])
ax9.set_ylim([-1, 1])
ax9.set_title('2010')
f.tight_layout()
pl.savefig('Indicator_correlations_US_vs_Ger_w_linregr.png')

#figure out which year has highest correlation coeff
yearly_stats=[]
for i in range(len(non_zero_pairs)):
    slope, intercept, r_value, p_value, std_err = linregress(non_zero_pairs[i][:,0],non_zero_pairs[i][:,1])
    yearly_stats.append([slope,intercept,r_value,p_value,std_err])
yearly_stats=np.array(yearly_stats)

pl.figure()
year_list=[i+1960 for i in range(len(yearly_stats))]
pl.plot(year_list,yearly_stats[:,2])
pl.title('Correlation coefficient over time')
pl.xlabel('Year')
pl.ylabel('Correlation coefficient')
#pl.axvline(x=1990,color='red')#1990, german reunification
#pl.text(1991,0.7,'German reunification',color='red')
pl.savefig('Yearly_correlation_coefficients_noline.png')
#correlation coefficient is how much two variables vary together (covariance) divided by product of their standard deviations:
#R = 1/(n-1)*1/(sig_x*sig_y)*(sum_x_y [(x-mean_x)(y-mean_y)])

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

pairs_by_indicator=np.array([norm_ray_us.T,norm_ray_ger.T]).T #indicator X year X 2
non_zero_inds=[]
for ind in pairs_by_indicator:
    pairs = [pair for pair in ind if (pair[0]!=0 and pair[1]!=0)]
    non_zero_inds.append(np.array(pairs))
#creates time series of indicators removing any pairs where any of the indicators is zero

indicator_stats=[]
for i,ind in enumerate(non_zero_inds):
    if len(ind)>20:#linear regression with less points is kind of moot
        slope, intercept, r_value, p_value, std_err = linregress(ind[:,0],ind[:,1])
        indicator_stats.append([slope, intercept, r_value, p_value, std_err])
    else:
        indicator_stats.append([0,0,0,0,0])

indicator_stats=np.array(indicator_stats)

slopes=indicator_stats[:,0]
r_vals=indicator_stats[:,2]
squared_r=r_vals**2 #pairwise square
sorted_squares=np.sort(squared_r)[::-1]
over09=np.argwhere(squared_r>0.9)
sorted_r=np.sort(r_vals)
sort_args=np.argsort(r_vals)[::-1]#highest correlation first

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

f, (topax, bottomax) = pl.subplots(2, 4)
#pl.title('USA vs. GER - correlated indicators over time')
xloc = pl.MaxNLocator(2)#max 3 ticks

#positive correlations
for i in range(4):
    us_nums = np.array(float_data_us)[sort_args[i]]
    us_nan = [num if num!=0 else np.nan for num in us_nums]
    print len(us_nan)
    topax[i].plot(year_list,us_nan,color='blue')
    ger_nums = np.array(float_data_ger)[sort_args[i]]
    ger_nan = [num if num!=0 else np.nan for num in ger_nums]
    print len(ger_nan)
    topax[i].plot(year_list,ger_nan,color='gold')
    short_title=indicator_list_us[sort_args[i]][0][:20]
    print short_title
    topax[i].set_title(short_title,size=10)
    topax[i].xaxis.set_major_locator(xloc)
    topax[i].axvline(x=1990,color='red')#1990, german reunification

#negative correlations
for i in range(4):
    us_nums = np.array(float_data_us)[sort_args[::-1][i]]
    us_nan = [num if num!=0 else np.nan for num in us_nums]
    print len(us_nan)
    bottomax[i].plot(year_list,us_nan,color='blue')
    ger_nums = np.array(float_data_ger)[sort_args[::-1][i]]
    ger_nan = [num if num!=0 else np.nan for num in ger_nums]
    print len(ger_nan)
    bottomax[i].plot(year_list,ger_nan,color='gold')
    short_title=indicator_list_us[sort_args[::-1][i]][0][:20]
    print short_title
    bottomax[i].set_title(short_title,size=10)    
    bottomax[i].xaxis.set_major_locator(xloc)
    bottomax[i].axvline(x=1990,color='red')#1990, german reunification

f.tight_layout()
pl.savefig('Indicator_top_correlations_US_vs_Ger_w_reunification_line.png')
