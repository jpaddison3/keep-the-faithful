## Keep The Faithful

Using data science to predict the attendance of churchgoers.

### The Opportunity

Many churches collect attendance, but usually have very crude - if any - uses for the data.  There is often quite a bit of information as churches keep age and gender for their demographic analysis, and attendance at many different types of events.  This project is an attempt to utilize the data from one church to predict churn of the churchgoers.  With the knowledge of who is likely to churn, we can intervene and keep people coming.

### Process
- People write their name in the attendance pad
- A volunteer enters the name into the database
- We query the database (not included) for csv files of users info and attendance
- Clean and select features
- Train a model
- Evaluate

### Features
- Age
- Recent attendance
- Years attending the church
- Number of family members
- Small group attendance

### Model

To deal with the imbalanced classes, the majority class is sampled down and minority is sampled up, to have the effect of weighting the classes.  This is done randomly multiple times and the resulting models are ensembled together to avoid throwing away data or overfitting.

### Results

The model predicts a collection of user ids that will churn.  Those will be converted to names and used by the pastors and volunteers to reach out to those on the list.  People love to talk to pastors and this gives the pastors an idea of how to direct their time in order to keep the faithful coming back to church.

The confusion matrix below shows the performance of the model on two test sets from different years. 

|                       |Predicted to Churn |Predicted to Stay |
| --------------------- |:-----------------:| ----------------:|
|**Actually Churned**   |40                 |78                |
|**Actually Stayed**    |99                 |1318              |

Compare to this matrix to the expected result with a random model:

|          Random       |Predicted to Churn |Predicted to Stay |
| --------------------- |:-----------------:| ----------------:|
|**Actually Churned**   |11                 |107               |
|**Actually Stayed**    |128                |1289              |

### Code organization

- `explore`

    - `explore.py` organizes by churn and prints features

- `keep_the_faithful`

    - `main.py` trains and evaluates a model
    
    - `sampled_forest.py` contains SampledForest model for unbalanced classes

    - `utilities` load and clean utilities

    - `feature-engineering` gives each user more predictive and standardized features that a model can take as inputs

Note: data is private.