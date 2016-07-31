# The World Bank World Development Indicators - Correlations across the globe

I chose to compare the development indicators of the World Bank for the US and Germany, which are the country I currently live in and my home country, respectively. I was interested to see both how correlated different indicators are (over time) and if there were years with more or less correlation between the indicators in the two countries.

The data is available at http://data.worldbank.org/country

The [World Bank](https://en.wikipedia.org/wiki/World_Bank) is an international financial institution with many functions, such as providing loans to developing countries, with the official goal to reduce poverty in the world.

The World Development Indicators (WDIs) are a set of over 1000 metrics published by the World Bank for every country or region, going back to 1960. The WDIs are used to assess the development of a country or region. Examples of WDIs are:

* Arable land (hectares)
* Net trades (US dollars)
* Infant mortality rate
* Electricity from renewables (kWh)
* CO_2 emissions (kt)
* etc.

The data can be downloaded directly from the [website](http://data.worldbank.org/country) as an excel or csv file for each country. This project works exclusively with the csv format (comma separated values). csv files for three countries (USA, Germany, Brazil) can be found in this repository. 

An example screenshot of the tabular data when viewed in your favorite spreadsheet viewer can be seen here:

![The data](images/data_screenshot.png)

Each of the 1000+ WDIs is listed from 1960 to 2015. As you can see the data is not perfectly clean. One of the major issues is missing data points. Many indicators are missing for certain (or all) years for a certain region. Additionally a variety of different units are used for the different metrics and each WDI can be on very different scales depending on the region or year, with smaller or bigger range of values depending on the region.

Data cleanup steps include:
* Identification of data rows/columns, removal or empty ones
* Removal of missing data points without “shifting” data (data point for 1970 needs to stay assigned to 1970 even if years before are removed)
* --> Solution: keep missing data points around as 0.0 and remove only when necessary
* When appropriate, data was scaled by subtracting average for that metric (over all years) and dividing by range (max-min) for that metric

All analysis was done with the following tools:
* Python
* Emacs
* Numpy (python library)
* Matplotlib (python library)
* Scipy (python library)
* csv (python library)

After scaling the different indicators for each country appropriately, we can now look at correlation plots for two countries in different years.

Here is what correlation plots look like for Germany and the United States, plotted for every five years.

![Germany-USA correlation plots](images/Indicator_correlations_US_vs_Ger.png)

As we can see correlations between the WDIs vary strongly for different years. To visualize the correlation for each year we can use linear regression (using scipy.stats):

![Germany-USA correlation plots](images/Indicator_correlations_US_vs_Ger_w_linregr.png)

The first plot shows a selection of years with 5 year intervals from 1970 to 2010. Each dot in each subplot represents on indicator's value normalized by subtracting the mean value of that indicator over all years and dividing by the range of the values for the indicator (for each country respectively). The US values are on the x axes and the German values are on the y axes. 

The second plot looks in more detail at the correlations between the two countries for different indicators. For that I calculated the correlations of the indicators between the two countries over time by linear regression. The plot shows the top 4 positively correlated indicators (Infant mortality rate, Under-5 mortality rate, CO2 emissions and Imports of goods and services, in that order) and the top 4 negatively correlated indicators (External balance on goods and services, Capture fisheries production, Total fisheries production and Net trade in goods, in that order.) For all plots the US is shown in blue and Germany in gold.
