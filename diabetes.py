import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

FILE_PATH = os.path.join("data", "diabetes_012_health_indicators_BRFSS2015-.csv")

def data_load(file):
    df = pd.read_csv(file)
    return df

#Cleaning data for visualization
def data_cleaning(df):
    df.dropna(inplace=True)

    df.rename(columns={
        "Diabetes_012": "DiabetesStatus",
        "HeartDiseaseorAttack": "HeartDisease",
        "HvyAlcoholConsump": "HeavyAlcoholConsumption",
        "NoDocbcCost": "NoDoctorBecauseCost",
        "GenHlth": "GeneralHealth",
        "MentHlth": "MentalHealthLast30D",
        "PhysHlth": "PhysicalHealthLast30D",
        "DiffWalk": "WalkingDifficulty"
    }, inplace=True)

    df.replace({"DiabetesStatus" : {0.0: "No diabetes", 1.0: "Pre diabetes", 2.0: "Diabetes"}},inplace=True)

    df.replace({"HighBP" : {0.0: "No high BP", 1.0: "High BP"}},inplace=True)

    df.replace({"HighChol" : {0.0: "No high cholesterol", 1.0: "High cholesterol"}},inplace=True)

    df.replace({"CholCheck" : {0.0: "No cholesterol check in 5 years", 1.0: "Yes cholesterol check in 5 years"}},inplace=True)

    df.replace({"Smoker" : {0.0: "No", 1.0: "Yes"}},inplace=True)

    df.replace({"Stroke" : {0.0: "No stroke", 1.0: "Had a stroke"}},inplace=True)

    df.replace({"HeartDisease" : {0.0: "No heart disease", 1.0: "Yes heart disease"}},inplace=True)

    df.replace({"PhysActivity" : {0.0: "No PhysActivity", 1.0: "Yes PhysActivity"}},inplace=True)

    df.replace({"Fruits" : {0.0: "No at least 1 fruit a day", 1.0: "Yes at least 1 fruit a day"}},inplace=True)

    df.replace({"Veggies" : {0.0: "No at least 1 veggie a day", 1.0: "Yes at least 1 veggie a day"}},inplace=True)

    df.replace({"HeavyAlcoholConsumption" : {0.0: "No heavy drinking", 1.0: "Yes heavy drinking"}},inplace=True)

    df.replace({"AnyHealthcare" : {0.0: "No coverage", 1.0: "Has coverage"}},inplace=True)

    df.replace({"NoDoctorBecauseCost" : {0.0: "No cost barrier", 1.0: "Cost prevented doctor visit"}},inplace=True)

    df.replace({"GeneralHealth" : {1.0: "Excellent GH", 2.0: "Very Good GH", 3.0: "Good GH", 4.0: "Fair GH", 5.0: "Poor GH"}},inplace=True)

    df["MentalHealthLast30D"] = df["MentalHealthLast30D"].apply(categorize_mentalhealth)

    df["PhysicalHealthLast30D"] = df["PhysicalHealthLast30D"].astype(int)

    df["PhysicalHealthLast30D"] = df["PhysicalHealthLast30D"].apply(format_physicalhealth)

    df.replace({"WalkingDifficulty" : {0.0: "No difficulty walking", 1.0: "Yes have difficulty walking"}},inplace=True)

    df.replace({"Sex": {0.0: "Female", 1.0: "Male"}},inplace=True)

    education_map = {
        1: "No School",
        2: "Elementary",
        3: "Some High School",
        4: "High School Grad",
        5: "Some College",
        6: "College Grad"
    }
    df["Education"] = df["Education"].map(education_map)

    income_map = {
        1: "Less than $10k",
        2: "$10k–$14,999",
        3: "$15k–$19,999",
        4: "$20k–$24,999",
        5: "$25k–$34,999",
        6: "$35k–$49,999",
        7: "$50k–$74,999",
        8: "Equal to or more than $75k"
    }
    df["Income"] = df["Income"].map(income_map)

    age_map = {
        1: "18–24",
        2: "25–29",
        3: "30–34",
        4: "35–39",
        5: "40–44",
        6: "45–49",
        7: "50–54",
        8: "55–59",
        9: "60–64",
        10: "65–69",
        11: "70–74",
        12: "75–79",
        13: "80+"
    }
    df["Age"] = df["Age"].map(age_map)
    return df

def categorize_mentalhealth(days):
    if days <= 5:
        return "Good, Less than 5 days"
    elif days <= 15:
        return "Moderate, less than 15"
    else:
        return "Poor, more than 15"

def format_physicalhealth(days):
    return f"{days}" + " Days"

#BAR GRAPH FOR THE DIABETES STATUS OF THE PEOPLE WHO TOOK THE SURVEY
def plot_diabetes_status(df):
    colors = ["seagreen", "darkred", "gold"]
    counts = df["DiabetesStatus"].value_counts()
    values = counts.values
    plt.bar(counts.index,counts.values,color=colors)
    plt.title('Diabetes Status Counts')
    for i, v in enumerate(values):
        plt.text(i, v+1000, str(v),ha="center", fontweight="bold")
    plt.xlabel('Diabetes Status')
    plt.ylabel('Count')
    plt.show()
    total = len(df)
    print(f"{total} People")
    print("In this survey")
    print(f"The number of people who doesnt have diabetes: {values[0]} and they are {round(values[0]/total*100,2)}%")
    print(f"The number of people who have diabetes: {values[1]} and they are {round(values[1]/total*100,2)}%")
    print(f"The number of people who have Pre diabetes: {values[2]} and they are {round(values[2]/total*100,2)}%")

#BAR GRAPH FOR THE SMOKERS AND HEART DISEASES AND STROKES
def plot_smokers_health(df):
    smokers_count = df[df["Smoker"] == "Yes"]["HeartDisease"].value_counts()
    smokers_count2 = df[df["Smoker"] == "Yes"]["Stroke"].value_counts()
    x_axis = ["Heart disease","Stroke"]
    y_axis = [smokers_count.values[1],smokers_count2.values[1]]
    plt.bar(x_axis, y_axis)
    for i, v in enumerate(y_axis):
        plt.text(i, v + 100, str(v), ha="center", fontweight="bold")
    plt.title("Smokers and health diseases")
    plt.xlabel('Diseases')
    plt.ylabel('Count')
    plt.show()
    print(f"The amount of smokers that had a heart disease: {smokers_count.values[1]}")
    print(f"The amount of smokers that had a stroke: {smokers_count2.values[1]}")

##BAR GRAPH FOR THE DIABETIC SMOKERS WITH HEART DISEASES OR STROKES
def plot_diabetic_smokers(df):
    diabetic_smoker = df[(df["Smoker"] == "Yes") & (df["HeartDisease"] == "Yes heart disease")]["DiabetesStatus"].value_counts()
    diabetic_smoker2 = df[(df["Smoker"] == "Yes") & (df["Stroke"] == "Had a stroke")]["DiabetesStatus"].value_counts()
    x_axis = ["Diabetic Smokers Heart disease","Diabetic Smokers Stroke"]
    y_axis = [diabetic_smoker.values[1],diabetic_smoker2.values[1]]
    plt.bar(x_axis, y_axis, color=["darkred", "gold"])
    for i, v in enumerate(y_axis):
        plt.text(i, v+100, str(v),ha="center", fontweight="bold")
    plt.title("Diabetic Smokers diseases")
    plt.xlabel("Diseases")
    plt.ylabel("Count")
    plt.show()
    total_diabetic_smokers = len(df[(df["Smoker"]=="Yes") & (df["DiabetesStatus"]=="Diabetes")])
    print(f"The amount of diabetic smokers with heart diseases is {diabetic_smoker.iloc[1]} and they are {round(diabetic_smoker.iloc[1]/total_diabetic_smokers*100,2)}% of the total diabetic smokers")
    print(f"The amount of diabetic smokers that had a stroke {diabetic_smoker2.iloc[1]} and they are {round(diabetic_smoker2.iloc[1]/total_diabetic_smokers*100,2)}% of the total diabetic smokers")

#Linechart for diabetes and age relation
def plot_age_diabetes(df):
    age_counts = df[df["DiabetesStatus"] == "Diabetes"]["Age"].value_counts()
    age_counts = age_counts.sort_index()
    plt.figure(figsize=(16, 7))
    plt.plot(age_counts.index, age_counts.values,marker="o",color="gold")
    plt.xlabel("Age")
    plt.ylabel("Counts of people with diabetes")
    plt.title("Correlation between age and diabetes")
    plt.grid(True)
    plt.show()
    print("People aged 50 and older have a higher incidence of diabetes, suggesting age is an important risk factor for diabetes.")

#BOXPLOT TO COMPARE THE BMI DISTRIBUTIONS ACROSS DIABETES STASUSES
def plot_bmi_boxplot(df):
    plt.figure(figsize=(7, 9))
    sns.boxplot(x="DiabetesStatus", y="BMI", hue="DiabetesStatus", data=df, palette="Set2", showfliers=False, legend=False)
    plt.ylim(15, 50)
    plt.title("BMI Distribution by Diabetes Status")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    print("There is a strong positive correlation between higher BMI and the likelihood of having diabetes. Individuals diagnosed with diabetes tend to have significantly higher BMI values compared to non-diabetic and pre-diabetic individuals.")
    print(df.groupby("DiabetesStatus")["BMI"].describe())

#HEATMAP CORRELATION FOR THE COLUMNS
def plot_correlation_heatmap(filepath):
    df2 = pd.read_csv(filepath)
    plt.figure(figsize=(16, 10))
    sns.heatmap(df2.select_dtypes(include=["number"]).corr(), annot=True, fmt=".3f")
    plt.xticks(fontsize=7)
    plt.yticks(fontsize=8)
    plt.show()
    corr_matrix = df2.corr(numeric_only=True)
    corr_melted = corr_matrix.reset_index().melt(id_vars='index')
    corr_melted.columns = ['Var1', 'Var2', 'Correlation']
    # Saving it as a Tableau-friendly CSV
    corr_melted.to_csv('correlation_matrix_long.csv', index=False)

def main():
    df = data_load(FILE_PATH)
    df = data_cleaning(df)
    df.to_csv("cleaned_diabetes_data.csv", index=False)
    plot_diabetes_status(df)
    plot_smokers_health(df)
    plot_diabetic_smokers(df)
    plot_age_diabetes(df)
    plot_bmi_boxplot(df)
    plot_correlation_heatmap(FILE_PATH)

if __name__ == "__main__":
    main()
