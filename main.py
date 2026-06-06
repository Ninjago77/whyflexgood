import pandas as pd


def grade(x:str):
    return int(x.strip().strip("Grade ")) # (int 8-12)


def often(x:str):
    return 5-([
    "Very often (3 or more times a week)",
    "Often (1-2 times a week)",
    "Sometimes (2-4 times a month)",
    "Rarely (2 or less times a month)",
    "Never"
    ].index(x.strip()))


def clean_ms_forms_checkboxes(df, column_name, allowed_values):
    """
    Parses an MS Forms checkbox column, keeps only allowed values,
    and deletes rows that become empty. Handles messy whitespace.
    """
    # 1. Clean the allowed values (strip whitespace and match casing strategy)
    allowed_set = {str(val).strip() for val in allowed_values}
    
    # Copy the dataframe to avoid SettingWithCopyWarning
    df = df.copy()
    
    # 2. Split and clean individual items
    def parse_and_filter(x):
        if pd.isnull(x):
            return []
        
        # Split by semicolon, then strip whitespace from EACH item
        raw_choices = [item.strip() for item in str(x).split(';')]
        
        # Filter against allowed set
        return [item for item in raw_choices if item in allowed_set]

    # Apply the cleaning logic
    df[column_name] = df[column_name].apply(parse_and_filter)
    
    # 3. Drop rows where the list is now empty and reset the index
    df = df[df[column_name].map(len) > 0].reset_index(drop=True)
    
    return df


def clean_ms_forms_single(df, column_name, allowed_values):
    """
    Cleans an MS Forms single-choice column, keeps only allowed values,
    and deletes rows that contain 'Other' or unexpected answers.
    """
    allowed_set = set(allowed_values)
    
    # 1. Keep the value if it is allowed, otherwise turn it into None/NaN
    df[column_name] = df[column_name].apply(
        lambda x: x if x in allowed_set else None
    )
    
    # 2. Drop rows where the column is now empty and reset index
    df = df[df[column_name].notnull()].reset_index(drop=True)
    
    return df


when = [
    "During Flex time",
    "Lunch",
    "After school",
    "I don't come in for help"
    ]

what = [
    "To do homework",
    "To study or ask for help",
    "To ask questions",
    "To meet with peers",
    "To work on other projects",
    "I don't use Flex time"
    ]

prevent = [
    "Availability of teachers",
    "Distractions in class. i.e. devices/people talking",
    "Communicating with peers",
    "Lack of energy or motivation",
    "Nothing prevents me from using flex time"
    ]

def how(x:str):
    return x.strip()


# Load data
# df = pd.read_csv("flex.csv",converters={
df = pd.read_excel('flex.xlsx', engine='openpyxl', converters={
    'grade': grade,
    "often": often,
    # "when": when,
    # "what": what,
    # "prevent": prevent,
    "how": how,
    # }, encoding='utf-8-sig')
    # }, encoding='cp1252')
    })


questions = {
    "grade": "What Grade are you in?",
    "often": "How often do you utilize your flex block to receive help with homework?",
    "when": "When do you usually come in for support with studies?",
    "what": "What do you use flex block for?",
    "prevent": "What prevents you most from using flex block to study/work on assignments?",
    "how": "How would you feel if flex time was removed?",
}

df = clean_ms_forms_checkboxes(df, "when", when)
df = clean_ms_forms_checkboxes(df, "what", what)
df = clean_ms_forms_single(df, "prevent", prevent)

df.to_excel('filename.xlsx', index=False)
# df.to_csv('filename.csv', index=False, encoding="utf-8")


#------------------------

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

plt.rcParams['figure.dpi'] = 150
# plt.style.use('seaborn-v0_8-whitegrid')
# --- Ensure this goes AFTER your existing data cleaning code ---

# 1. Prepare data for columns containing lists (checkboxes)
# .explode() creates a separate row for each item in the list, allowing accurate value counts
df_when_exploded = df.explode('when')
df_what_exploded = df.explode('what')

# ==========================================
# PIE CHARTS
# ==========================================
# Pie Chart: Grade Distribution
# plt.figure(figsize=(8, 6))
# df['grade'].value_counts().plot.pie(autopct='%1.1f%%', startangle=140, cmap='Pastel1')
# plt.title('Distribution of Students by Grade')
# plt.ylabel('') # Hides the y-label for a cleaner look
# plt.legend()
# plt.show()

# # Pie Chart: What prevents students from using Flex block?
# plt.figure(figsize=(10, 8))
# df['prevent'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, cmap='Set3')
# plt.title('What Prevents Students from Using Flex Block?')
# plt.ylabel('')
# plt.legend()
# plt.tight_layout()
# plt.show()
# ==========================================
# BAR CHARTS (Multiple Choice/Checkboxes)
# ==========================================

# # Horizontal Bar Chart: What is Flex block used for?
# plt.figure(figsize=(10, 6))
# df_what_exploded['what'].value_counts().sort_values().plot.barh(color='skyblue')
# plt.title('What Students Use Flex Block For')
# plt.xlabel('Number of Mentions')
# plt.ylabel('')
# plt.tight_layout()
# plt.show()

# # Bar Chart: When do students come in?
# plt.figure(figsize=(8, 6))
# df_when_exploded['when'].value_counts().plot.bar(color='lightgreen', rot=45)
# plt.title('When Students Seek Support')
# plt.ylabel('Number of Mentions')
# plt.xlabel('')
# plt.tight_layout()
# plt.show()

# # Horizontal Bar Chart: What is Flex block used for?
# plt.figure(figsize=(10, 6))
# counts_what = df_what_exploded['what'].value_counts().sort_values()
# colors_what = [plt.cm.tab10(i % 10) for i in range(len(counts_what))]

# # Plot the bars
# bars_what = plt.barh(counts_what.index, counts_what.values, color=colors_what)

# plt.title('What Students Use Flex Block For')
# plt.xlabel('Number of Mentions')
# plt.ylabel('')

# # Generate legend handles matching each specific category to its color
# plt.legend(handles=bars_what, labels=list(counts_what.index), loc='lower right')
# plt.tight_layout()
# plt.show()


# # Bar Chart: When do students come in?
# plt.figure(figsize=(8, 6))
# counts_when = df_when_exploded['when'].value_counts()
# colors_when = [plt.cm.Set2(i % 8) for i in range(len(counts_when))]

# # Plot the bars
# bars_when = plt.bar(counts_when.index, counts_when.values, color=colors_when)

# plt.title('When Students Seek Support')
# plt.ylabel('Number of Mentions')
# plt.xlabel('')
# plt.xticks(rotation=45)

# # Generate legend handles matching each specific category to its color
# plt.legend(handles=bars_when, labels=list(counts_when.index), loc='upper right')
# plt.tight_layout()
# plt.show()
# # ==========================================
# # COMPARISONS & CORRELATIONS
# # ==========================================

# Comparison 1: Average 'Often' score by Grade
# Shows which grades utilize flex time the most on average
# plt.figure(figsize=(8, 6))
# df.groupby('grade')['often'].mean().sort_index().plot.bar(color='coral')
# plt.title('Average Frequency of Flex Time Usage by Grade\n(1 = Never, 5 = Very Often)')
# plt.xlabel('Grade')
# plt.ylabel('Average Frequency Score')
# plt.ylim(0, 5) # Lock scale to 1-5 range
# plt.xticks(rotation=0)
# plt.tight_layout()
# plt.show()

# # Comparison 2: Stacked Bar - Prevention reasons broken down by Grade
# # Shows if certain grades face specific barriers more than others
# cross_tab_prevent = pd.crosstab(df['grade'], df['prevent'])
# cross_tab_prevent.plot(kind='bar', stacked=True, figsize=(12, 8), cmap='tab20')
# plt.title('Barriers to Using Flex Time by Grade')
# plt.xlabel('Grade')
# plt.ylabel('Number of Students')
# plt.xticks(rotation=0)
# plt.legend(title='Prevention Reason', bbox_to_anchor=(1.05, 1), loc='upper left')
# plt.tight_layout()
# plt.show()

# # Comparison 3: Usage ('what') broken down by Grade
# cross_tab_what = pd.crosstab(df_what_exploded['grade'], df_what_exploded['what'])
# cross_tab_what.plot(kind='bar', figsize=(14, 8), cmap='Set2')
# plt.title('Flex Time Activities by Grade')
# plt.xlabel('Grade')
# plt.ylabel('Number of Mentions')
# plt.xticks(rotation=0)
# plt.legend(title='Activity', bbox_to_anchor=(1.05, 1), loc='upper left')
# plt.tight_layout()
# plt.show()

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------

# Ensure grades are treated as integers for correct sorting
df['grade'] = df['grade'].astype(int)
# df_what_exploded = df.explode('what')

# ==========================================
# VARIATION 1: 100% Stacked Bar (Prevention Reasons)
# ==========================================
# normalize='index' changes absolute counts into proportions (0.0 - 1.0) per grade
# prevent_pct = pd.crosstab(df['grade'], df['prevent'], normalize='index') * 100

# prevent_pct.plot(kind='bar', stacked=True, figsize=(12, 8), cmap='tab20')
# plt.title('What Prevents Students From Using Flex Time (Percentage per Grade)')
# plt.xlabel('Grade')
# plt.ylabel('Percentage of Students (%)')
# plt.ylim(0, 100)
# plt.xticks(rotation=0)
# plt.legend(title='Prevention Reason', bbox_to_anchor=(1.05, 1), loc='upper left')
# plt.tight_layout()
# plt.show()

# ==========================================
# VARIATION 2: Grouped Bar (Flex Activities - % of Total Selections)
# ==========================================
# Shows how the "pie" of activities is split up within each grade
# what_pct_selections = pd.crosstab(df_what_exploded['grade'], df_what_exploded['what'], normalize='index') * 100

# what_pct_selections.plot(kind='bar', figsize=(14, 8), cmap='Set2')
# plt.title('Flex Time Activities (Share of Total Selections per Grade)')
# plt.xlabel('Grade')
# plt.ylabel('Percentage of Total Selections (%)')
# plt.xticks(rotation=0)
# plt.legend(title='Activity', bbox_to_anchor=(1.05, 1), loc='upper left')
# plt.tight_layout()
# plt.show()

# ==========================================
# VARIATION 3: Grouped Bar (Flex Activities - % of Actual Students)
# ==========================================
# Since it's a checkbox, this calculates: (How many kids said X) / (Total kids in that grade)
# Note: Because students can pick multiple answers, columns will NOT add up to 100%

# counts_what = pd.crosstab(df_what_exploded['grade'], df_what_exploded['what'])
# students_per_grade = df['grade'].value_counts()
# what_pct_students = counts_what.div(students_per_grade, axis=0) * 100

# what_pct_students.plot(kind='bar', figsize=(14, 8), cmap='Accent')
# plt.title('Percentage of Students in Each Grade Who Select Each Activity\n(Bars represent % of actual students; can exceed 100% total due to checkboxes)')
# plt.xlabel('Grade')
# plt.ylabel('Percentage of Students in Grade (%)')
# plt.xticks(rotation=0)
# plt.legend(title='Activity', bbox_to_anchor=(1.05, 1), loc='upper left')
# plt.tight_layout()
# plt.show()




# counts_when = pd.crosstab(df_when_exploded['grade'], df_when_exploded['when'])
# students_per_grade = df['grade'].value_counts()
# when_pct_students = counts_when.div(students_per_grade, axis=0) * 100

# when_pct_students.plot(kind='bar', figsize=(14, 8), cmap='Accent')
# plt.title('Percentage of Students in Each Grade Who Select Each Support Time\n(Bars represent % of actual students; can exceed 100% total due to checkboxes)')
# plt.xlabel('Grade')
# plt.ylabel('Percentage of Students in Grade (%)')
# plt.xticks(rotation=0)
# plt.legend(title='Support Time', bbox_to_anchor=(1.05, 1), loc='upper left')
# plt.tight_layout()
# plt.show()

#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################
############################# ADVANCED #####
#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################

import seaborn as sns

# Explode both columns to create a Cartesian product for each student
# (e.g., if a student picks 2 'what's and 2 'when's, it maps all 4 combinations)
df_combinations = df[['what', 'when']].copy()
df_combinations = df_combinations.explode('what').explode('when')

# Create a cross-tabulation matrix
co_occurrence = pd.crosstab(df_combinations['what'], df_combinations['when'])

plt.figure(figsize=(10, 6))
sns.heatmap(co_occurrence, annot=True, fmt='d', cmap='Blues', linewidths=.5)
plt.title('Activity vs. Time: When are specific tasks happening?')
plt.xlabel('When they seek support')
plt.ylabel('What flex time activities they do')
plt.tight_layout()
plt.show()



######


plt.figure(figsize=(12, 6))
# Calculate the average 'often' score for each prevention reason, sorted descending
avg_often_by_prevent = df.groupby('prevent')['often'].mean().sort_values(ascending=False)

# Create a bar chart with a color gradient based on the score
ax = sns.barplot(
    x=avg_often_by_prevent.values, 
    y=avg_often_by_prevent.index, 
    palette='magma'
)

# Add a vertical line for the overall school average frequency
overall_avg = df['often'].mean()
plt.axvline(overall_avg, color='red', linestyle='--', label=f'School Average ({overall_avg:.2f})')

plt.title('What prevents the most? : Average Flex Usage Frequency by Flex Attendance Prevention')
plt.xlabel('Average Frequency Score (1 = Never, 5 = Very Often)')
plt.ylabel('What prevents them?')
# Dynamically extract the colors used by Seaborn to create matching legend patches
colors = [patch.get_facecolor() for patch in ax.patches]
category_patches = [
    mpatches.Patch(color=color, label=label)
    for label, color in zip(avg_often_by_prevent.index, colors)
]

# Combine the school average line handle with the new category patches for the legend
handles, labels = ax.get_legend_handles_labels()
plt.legend(handles=handles + category_patches, bbox_to_anchor=(1, 0), loc='lower right')
plt.xlim(1, 5)
plt.tight_layout()
plt.show()



########



# Calculate how many different activities each student selected
df['activity_count'] = df['what'].apply(len)

plt.figure(figsize=(10, 6))
# Boxplot shows the distribution of frequency scores based on how many activities they chose
sns.boxplot(x='activity_count', y='often', data=df, palette='Set3')
sns.stripplot(x='activity_count', y='often', data=df, color=".25", alpha=0.5, jitter=True)

plt.title('Usage Breadth: Does having more reasons to attend increase frequency?')
plt.xlabel('Number of Different Activities Selected')
plt.ylabel('Frequency Score (1-5)')
plt.tight_layout()
plt.show()



######

# Pivot table calculating the mean 'often' score for every Grade + Barrier combination
pivot_often = pd.pivot_table(
    df, 
    values='often', 
    index='prevent', 
    columns='grade', 
    aggfunc='mean'
)

plt.figure(figsize=(12, 7))
# Use a diverging colormap so lower scores are red/orange, high scores are green/blue
sns.heatmap(pivot_often, annot=True, fmt=".1f", cmap='RdYlGn', center=df['often'].mean(), linewidths=.5)
plt.title("Flex Usage & Barriers: Average Frequency by Grade and Prevention Reason")
plt.xlabel('Grade')
plt.ylabel('What prevents them?')
plt.tight_layout()
plt.show()


#####

from matplotlib_venn import venn2 
# (You may need to `pip install matplotlib-venn` if you don't have it)

# Create sets of indices for students who do homework vs students who study
hw_users = set(df[df['what'].apply(lambda x: 'To do homework' in x)].index)
study_users = set(df[df['what'].apply(lambda x: 'To study or ask for help' in x)].index)

plt.figure(figsize=(8, 6))
venn2(
    [hw_users, study_users], 
    set_labels=('To do homework', 'To study/ask for help'),
    set_colors=('skyblue', 'lightgreen')
)
plt.title('Overlap of Academic Users: Homework vs. Studying')
plt.tight_layout()
plt.show()