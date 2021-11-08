# data

This dataset includes 
* 2019 5-year estimates at the metropolitan statistical area level from the [American Community Survey](https://data.census.gov/cedsci/) 
* obesity rates at the county level from the [CDC](https://gis.cdc.gov/grasp/diabetes/DiabetesAtlas.html)

"metropolitan statistical area" is a technical term - an MSA can span more than one county. Inferring obesity rates for an MSA by extrapolating from the county isn't straightforward, but I did my best.

While the ACS data can get pretty detailed, they forbid you from conditioning on many variables at once, because of informational entropy. We might be very interested in how many unmarried non-Hispanic white women between the ages of 20-24 make between $40-80k, but in a small enough area that might uniquely identify somebody. So they make a tradeoff between the size of the area and the depth of the statistic. 

Some of the columns may be kind of confusing:
* p_gay - this is the % of same-sex households where the householder is male. it's not perfect, or even very good, but it does seem to be higher in areas known to be gay a priori.
* p_white_unmarried - this is the % of white people who are unmarried, NOT the % of unmarried people who are white. not gonna fix the column name, you're lucky i'm writing this at all.
* p_hapa - yup, this is the % of people who are half asian half white. 
* p_unmarried_20_24_female - out of unmarried people between the ages of 20 and 24 inclusive, what % of them are female? For ~90% of areas, this is actually less than 50%. It's probably not that the survey methodology is flawed; 23 year old women get married to 25 year old men.
