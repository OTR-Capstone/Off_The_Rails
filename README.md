# Off The Rails 
by: David Berchelmann, Steve Kane, Justin Sullivan, and Gabriela Tijerina 
****

### Project Summary:
Our team accessed the U.S. Department of Transportation’s database to analyze 8 years of rail accidents across the United States. We utilized the full data science pipeline to analyze the data and create a classification model that would predict which company would be involved in a rail accident.


**Data Source:** U.S. Department of Transportation 
****

### Project Goals:

- Determine which features are drivers of highway rail accidents and equipment rail accidents.
- Build a classification model for predicting which Railroad operator is most likely to be involved with a given accident. This information is used to enhance the overall analysis.

**** 

### Deliverables:
- Showcase highlighted findings in a presentation delivered to stakeholders. 
- Create a reproducible jupyter notebook report that includes process, takeaways, and discoveries from every stage of the pipeline. 
**** 

### Initial Hypotheses:

- For each type of rail incidents, Railroad Operator plays into the frequency of incidents and the severity of incidents. 
- Geography and location has an impact on the type of rail incident.
- Time of year and weather conditions have an impact on the frequency and scale of a rail accident.
- There will be a difference in severity of accident based on whether the accident was a highway rail accident or an equipment accident.


****

### Data Dictionary


| Features    | Description             | Data Type |
|-------------|-------------------------|-----------|
| iyr         | year of incident        | 
| imo         | month of incident       |
| railroad    | 
| state       | FIPS state code         |
| temp        | temp in degrees         |
| visibility  | daylight period         |
| weather     | weather conditions      |
| trnspd           | int
| typspd.        | object
| trnbbr | object
| trndir | float
| tons | int
| typeq | object
| trkname | object
| typtrk | int
| headend1 | int
| loadf1 | int 
| loadp1| int
| emptyf1 | int
| emptyp1 | int 
| eqpdmg | int 
| trkdmg | int 
| cause | object
| caskldrr | int 
| casinjrr | int
| caskld | int
| casinj | int
| highspd | int
| 



\* - Indicates the target feature in this data
***


### Data Science Pipeline:

#### 1. Acquire
- The data is acquired from csv files sourced from the US Department of Transportation.
- Two datframes are created by concatenting the csv files for highway rail accidents and equipment rail accidents. 

#### 2. Prepare
- Prepare the data for analysis with two prepare modules, one for each type of rail incident (highway  and equipment)
- The prepare modules will return respective dataframes, split into train, validate and test. The train dataset will be ready for explorary analysis. 

#### 3. Explore & Preprocessing
- Exploration is reprodible and takeaways are well documented.
- Preprocessing module prepares the dataframes for modeling.

#### 4. Model/Evaluate
- Develop a baseline model for predicting the railroad operator based on the type of indcident and incident features
- Build classification models that improve upon the baseline accuracy with the understanding that model performance and evaluation metrics will better inform the overall analysis. 

#### 5. Deliver
- A deployed model that can take in new data that is preprocessed and returns similar results. This is important for supporting any analysis and takeaways that were concluded from the modeling stage. 
- A report with visuals that highlight the findings from the project analysis
- A reproducible notebook that is well-documented


### Conclusion:


### Next Steps: 


****

### Instructions for Reproducing Project:  

1.  Read and follow this README.md. 

2.  Download the following files to your working directory:  

3.  Run our final Jupyter Notebook to reproduce our findings and analysis. 