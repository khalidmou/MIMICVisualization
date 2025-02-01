import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import altair as alt




#################MICROBIOLOGYEVENTS.csv################
microbiology_data = pd.read_csv('mimic_3/MICROBIOLOGYEVENTS.csv')
event_counts = microbiology_data['ab_name'].value_counts()
plt.pie(event_counts, labels=event_counts.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
plt.title('Proportion of Event Types')
plt.show()
###################SERVICES.CSV################
file_path = "mimic_3/SERVICES.csv"
df = pd.read_csv(file_path)
df['transfertime'] = pd.to_datetime(df['transfertime'], errors='coerce')  # Convert to datetime
df['month'] = df['transfertime'].dt.month  # Extract the month
grouped = df.groupby(['curr_service', 'month']).size().reset_index(name='count')
services = grouped['curr_service'].unique()
months = grouped['month'].unique()
service_map = {service: i for i, service in enumerate(services)}
x = grouped['month'].map(lambda m: months.tolist().index(m))  # X-axis: Months
y = grouped['curr_service'].map(lambda s: service_map[s])  # Y-axis: Services
z = grouped['count']
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
sc = ax.scatter(x, y, z, c=z, cmap='viridis', s=100)
ax.set_xlabel('Month')
ax.set_ylabel('Current Service')
ax.set_zlabel('Count')
cb = plt.colorbar(sc, ax=ax, shrink=0.6)
cb.set_label('Count')
ax.set_xticks(range(len(months)))
ax.set_xticklabels(months)
ax.set_yticks(range(len(services)))
ax.set_yticklabels(services)

plt.title('Monthly Distribution of Current Service')
plt.show()
#####################  Merging PRESCRIPTION.csv and  PATIENTS.csv
perscriptions = pd.read_csv("mimic_3/PRESCRIPTIONS.csv")
patients = pd.read_csv("mimic_3/patients.csv")
df = pd.merge(patients, perscriptions, on='subject_id', how='inner')
df['startdate'] = pd.to_datetime(df['startdate'], errors='coerce')
df['enddate'] = pd.to_datetime(df['enddate'], errors='coerce')
df['stay_length'] = (df['enddate'] - df['startdate']).dt.days
gender_stats = df.groupby('gender')['stay_length'].agg(['mean', 'sum']).reset_index()
plt.figure(figsize=(10, 6))
plt.bar(gender_stats['gender'], gender_stats['mean'], color=['blue', 'pink'], alpha=0.7)
plt.title('Average Prescription Period per Gender')
plt.xlabel('Gender')
plt.ylabel('Average Duration (Days)')
plt.xticks(ticks=range(len(gender_stats['gender'])), labels=gender_stats['gender'])
plt.show()
##################################################PATIENTS TRANSFER####################
patients = pd.read_csv("mimic_3/patients.csv")
transfers = pd.read_csv("mimic_3/transfers.csv")
patients['dob'] = pd.to_datetime(patients['dob'], errors='coerce')
transfers['intime'] = pd.to_datetime(transfers['intime'], errors='coerce')
data = pd.merge(transfers, patients, on='subject_id')
admit_data = data[data['eventtype'].str.lower() == 'admit']
admit_data['intime'] = admit_data['intime'].dt.date
admit_data['dob'] = admit_data['dob'].dt.date
admit_data['age_at_admit'] = (admit_data['intime'] - admit_data['dob']).apply(lambda x: x.days)//365
admit_data = admit_data[(admit_data['age_at_admit'] >= 0) & (admit_data['age_at_admit'] <= 120)]
plt.figure(figsize=(10, 6))
sns.histplot(
    admit_data['age_at_admit'],
    bins=20,
    kde=True,
    color='blue',
    edgecolor='black'
)
plt.title('Age Distribution of Patients at Admission', fontsize=16)
plt.xlabel('Age at Admission', fontsize=14)
plt.ylabel('Number of Patients', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

#######################  ADMISSION     #######################################
admissions = pd.read_csv("mimic_3/admissions.csv")
admissions['admittime'] = pd.to_datetime(admissions['admittime'])
admissions['year_month'] = admissions['admittime'].dt.to_period('M')
monthly_admissions = admissions.groupby('year_month').size()
plt.figure(figsize=(12, 6))
sns.lineplot(x=monthly_admissions.index.astype(str), y=monthly_admissions.values)
plt.title("Monthly Admissions Over Time")
plt.xlabel("Month")
plt.ylabel("Number of Admissions")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
####################### PATIENTS #######################
df = pd.read_csv('mimic_3/ADMISSIONS.csv')
ethnicity_insurance_counts = df.groupby(['ethnicity', 'insurance']).size().reset_index(name='count')
plt.figure(figsize=(12, 6))
sns.barplot(x="ethnicity", y="count", hue="insurance", data=ethnicity_insurance_counts)
plt.title("Ethnicity by Insurance Type")
plt.xlabel("Ethnicity")
plt.ylabel("Number of Patients")
plt.xticks(rotation=45)
plt.legend(title="Insurance Type")
plt.show()