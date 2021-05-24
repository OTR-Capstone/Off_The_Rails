

<div align="center"><img width="500" height="500" src="https://i.ibb.co/2yG1ZbR/Minimal-Cat-and-Book-Line-Art-Illustration-Logo.png" /></div>


****

[[Project Summary](#project_summary)]
[[Project Goals](#goals)]
[[Deliverables](#deliverables)]
[[Project Planning](#planning)]
[[Initial Hypothesis](#hypo)]
[[Equipment Rail Data Dictionary](#equipdic)]
[[Highway Rail Data Dictionary](#hwydic)]
[[FIPS State Codes](#fipsdic)]
[[DS Pipeline](#dspipe)]
[[Conclusion](#findings)]
[[Next Steps](#next)]
[[Reproduce This Project](#reproduce)]
​
​



### <a name="project_summary"></a>Project Summary:
Our team accessed the U.S. Department of Transportation’s database to analyze 8 years of rail accidents across the United States. We utilized the full data science pipeline to analyze the data and create a classification model that would predict which company would be involved in a rail accident.


**Data Source:** U.S. Department of Transportation 
****

### <a name="goals"></a> Project Goals:

- Determine which features are drivers of highway rail accidents and equipment rail accidents.
- Build a classification model for predicting which Railroad operator is most likely to be involved with a given accident. This information is used to enhance the overall analysis.

**** 

### <a name="deliverables"></a> Deliverables:
- Showcase highlighted findings in a presentation delivered to stakeholders. 
- Create a reproducible jupyter notebook report that includes process, takeaways, and discoveries from every stage of the pipeline. 
**** 

### <a name="planning"></a> Project Planning:

All of our project planning can be found on Trello. Below is a link to our progress along with a visual snapshot.


A link to the Trello board below can be found at https://trello.com/b/msJXyeEv/off-the-rails


Here is a snapshot of our project planning/setup on the evening of 5/23/21

<img src="https://i.ibb.co/RpGfnfb/Screen-Shot-2021-05-23-at-19-23-15.png" alt="Reg-ppline" border="2">

****

### <a name="hypo"></a> Initial Hypotheses:

- For each type of rail incidents, Railroad Operator plays into the frequency of incidents and the severity of incidents. 
- Geography and location has an impact on the type of rail incident.
- Time of year and weather conditions have an impact on the frequency and scale of a rail accident.
- There will be a difference in severity of accident based on whether the accident was a highway rail accident or an equipment accident.


****

### <a name="dictionary"></a> Data Dictionary
\* - Indicates the target feature in this data

### <a name="equipdic"></a> Equipment Data

| Features            | Description                   | Data Type |
|---------------------|-------------------------------|-----------|
| railroad_company *  | railroad code                 | object    |
| accident_type       | type of accident              | int       |
| state               | FIPS state code               | int       |
| temp                | temp in degrees               | int       |
| visibility          | encoded visibility            | int       |
| weather             | weather conditions            | int       |
| train_speed         | speed of train in mph         | int       |
| train_direction     | train direction               | float     |
| train_weight        | gross tonnage of train        | int       |
| train_type          | type of equipment             | object    |
| track_type          | type of track                 | int       |
| front_engines       | # of head end locomotives     | int       |
| loadfrght_cars      | # of loaded freight cars      | int       |
| loadpass_cars       | # of loaded passenger cars    | int       |
| emptyfrght_cars     | # of empty freight cars       | int       |
| emptypass_cars      | # of empty passenger cars     | int       | 
| equip_damage        | equipment damage is USD       | int       |
| track_damage        | track damage in USD           | int       |
| cause               | cause of incidence            | object    |
| total_killed        | # of killed                   | int       | 
| total_injured       | # of injured                  | int       |
| max_speed           | maximum equipment speed       | int       |
| total_damage        | total damage                  | int       |
| engineers_onduty    | # of engineers on duty        | float     |
| conductors_onduty   | # of conductors on duty       | float     |
| brakemen_onduty     | # of brakemen on duty         | float     |
| region              | FRA designated region         | int       |
| typrr               | type of railroad              | object    |
| lat                 | latitude                      | object    |
| long                | longitude                     | object    |
| signal_type         | type of signal                | int       |
| date                | date of incident              | datetime  |
| season              | season of year                | object    |

### <a name="hwydic"></a> Highway Data

| Features            | Description                   | Data Type |
|---------------------|-------------------------------|-----------|
| railroad_company *  | railroad code                 | object    |
| station             | nearest timeable station      | object    |
| county              | FIPS county code              | object    |
| state               | FIPS state code               | int       |
| region              | FRA designated region         | int       |
| city                | FIPS city code                | object    |
| vehicle_speed       | estimated vehicle speed       | float     |
| vehicle_type        | encoded highway user          | object    |
| vehicle_direction   | encoded user direction        | object    |
| position            | encoded user direction        | object    |
| accident_type       | circumstance of accident      | int       |
| hazmat_entity       | entity transporting hazmat    | object    |
| temp                | temperature in degrees        | int       |
| visibility          | encoded visibility            | int       |
| weather             | weather conditions            | object    |
| train_type          | type of equipment             | object    |
| track_type          | type of track                 | object    |
| front_engines       | # of head end locomotives     | int       |
| railcar_quantity    | quantity of railcar           | int       |
| train_speed         | estimated train speed         | float     |
| train_direction     | direction of train            | object    |
| warning_location    | location of warning           | object    |
| warning_signal      | crossing w highway signal     | object    |
| lights              | crossing illuminated          | object    |
| standveh            | passed a standing vehicle     | object    |
| other_train         | another train involved        | object    |
| motorist_action     | action of highway user        | object    |
| view_obstruction    | track view obstruction        | int       |
| vehicle_damage      | vehicle damage in USD         | float     |
| driver_fate         | fate of driver                | object    |
| vehicle_occupied    | was the vehicle occupied      | object    |
| total_killed        | total # of deaths             | int       |
| total_injured       | total # of deaths             | int       |
| vehicle_occupants   | # of vehicle occupants        | int       |
| ispublic_crossing   | is this a public crossing     | object    |
| fips                | FIPS code                     | int       |
| whistle_ban         | whistle ban in effect         | object    |
| driver_age          | age of driver                 | object    |
| driver_gender       | gender of driver              | object    |
| train_occupants     | # people on train             | int       |
| user_killed         | # of drivers killed           | int       |
| user_injured        | # of drivers injured          | int       |
| rail_killed         | # of rr employess killed      | int       |
| rail_injured        | # of rr employees injured     | int       |
| train_pass_killed   | # train passengers killed     | int       |
| train_pass_injured  | # train passengers injured    | int       |
| road_conditions     | encoded road conditions       | object    |
| date                | date of incident              | datetime  |
| season              | season of year                | object    |

### <a name="fipsdic"></a> FIPS State Codes

| FIPS Code   | Corresponding State                 
|-------------|------------------------|
| 01          | Alabama                |
| 02          | Alaska                 |
| 04          | Arizona                |
| 05          | Arkansas               |
| 06          | California             |
| 08          | Colorado               |
| 09          | Connecticut            |
| 10          | Delaware               |
| 11          | District of Columbia   |
| 12          | Florida                |
| 13          | Georgia                |
| 15          | Hawaii                 |
| 16          | Idaho                  |
| 17          | Illinois               |
| 18          | Indiana                |
| 19          | Iowa                   |
| 20          | Kansas                 |
| 21          | Kentucky               |
| 22          | Louisiana              |
| 23          | Maine                  |
| 24          | Maryland               |
| 25          | Massachusetts          |
| 26          | Michigan               |
| 27          | Minnesota              |
| 28          | Mississippi            |
| 29          | Missouri               |
| 30          | Montana                |
| 31          | Nebraska               |
| 32          | Nevada                 |
| 33          | New Hampshire          |
| 34          | New Jersey             |
| 35          | New Mexico             |
| 36          | New York               |
| 37          | North Carolina         |
| 38          | North Dakota           |
| 39          | Ohio                   |
| 40          | Oklahoma               |
| 41          | Oregon                 |
| 42          | Pennsylvania           |
| 44          | Rhode Island           |
| 45          | South Carolina         |
| 46          | South Dakota           |
| 47          | Tennessee              |
| 48          | Texas                  |
| 49          | Utah                   |
| 50          | Vermont                |
| 51          | Virginia               |
| 53          | Washington             |
| 54          | West Virginia          |
| 55          | Wisconsin              |
| 56          | Wyoming                |



***


### <a name="dspipe"></a> Data Science Pipeline:

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


### <a name="findings"></a> Conclusion:


### <a name="next"></a> Next Steps: 


****

### <a name="reproduce"></a> Instructions for Reproducing Project:  

1.  Read and follow this README.md. 

2.  Download the following files to your working directory:  

3.  Run our final Jupyter Notebook to reproduce our findings and analysis. 