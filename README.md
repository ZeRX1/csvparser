#Current priority:

- [x] - Use it as script with arguments (!)
    - [x] - Make help
    - [ ] - (test) First time setup thing, if the script doesn't detect a config file (.env; config.ini) it'll create one and ask for data needed for the script to run (DB ip, token, org, what buckets etc.) and save them
    - [x] - Make an option of config that will save it in a config.json file where you'd specify what data do you want. If there's a need to only read one thing then use the arguments


- [X] - Parsing the data in Python (!)

- [X] !- Using numpy, pandas to build data frames (!)
    - [Tutorial for this](https://www.geeksforgeeks.org/create-a-dataframe-from-a-numpy-array-and-specify-the-index-column-and-column-headers/)
    - [x] - Make seperate dataframes for each table
    - [x] - Join the dataframes
    - [x] - Make a function to join data frames without hard-coded things
    - [ ] - Make a function to give an array of column names for plotting
    
- [x] !- Using Matplotlib or Seaborn to plot the data and the frequency
    - [Tutorial for this](https://medium.com/ml-with-arpit-pathak/data-visualization-using-matplotlib-and-seaborn-in-python-62fd64a57936)
    - [x] - Plot merged data frame
    - [x] - Add labels and title
    - [ ] - Make it universal (!)

- [x] ?- The plotted data should be load cell data, as well as wind parameters such as aws.
        - nmea2k aws/awd
        - downsampled

- [x] - Make a proper table that will hold everything that's pulled from the database
        - [x] - Pull the data directly and put it into a table from which we make a dataframe

- [ ] - Jupyter Notebook integration (!)

- [ ] - Function to get the data from database with choosing exact data, if not then print out the whole
    - [ ] - Pull choosen data from db directly (If args are present use them instead of .env)
    - [ ] - Make queries to db as a function



- ParseDataFrames:

    1. Make a table with one measurement (filter the first one for example)
    2. Make it universal (pull the list of the names matching for what you want, by function argument)
    3. Make a dataframe for each measurement in a bucket
    4. join the buckets with outer join with timestamp as a key

    - downsampled:
        - Headstay
        - V1P
        - V1S

    - nmea2k:
        - aws
        - awd

    *2 - check if possible while still maintaining more or less efficient code

    *additional - Try to make it more or less efficient (no more than 5-10 seconds to pull from db (probably filters would help)) and try to use the most of the db

    - Do some things with this:
    [IoT help from David](https://github.com/david-marti/IoT__exercise)