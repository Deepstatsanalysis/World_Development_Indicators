# data_incubator

I chose to compare the development indicators of the World Bank for the US and Germany, which are the country I currently live in and my home country, respectively. I was interested to see both how correlated different indicators are (over time) and if there were years with more or less correlation between the indicators in the two countries.

The data is available at http://data.worldbank.org/country

The first plot shows a selection of years with 5 year intervals from 1970 to 2010. Each dot in each subplot represents on indicator's value normalized by subtracting the mean value of that indicator over all years and dividing by the range of the values for the indicator (for each country respectively). The US values are on the x axes and the German values are on the y axes. 

The second plot looks in more detail at the correlations between the two countries for different indicators. For that I calculated the correlations of the indicators between the two countries over time by linear regression. The plot shows the top 4 positively correlated indicators (Infant mortality rate, Under-5 mortality rate, CO2 emissions and Imports of goods and services, in that order) and the top 4 negatively correlated indicators (External balance on goods and services, Capture fisheries production, Total fisheries production and Net trade in goods, in that order.) For all plots the US is shown in blue and Germany in gold.
