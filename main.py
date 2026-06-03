import pandas as pd
import matplotlib.pyplot as plt


def grade(x:str):
    return x.strip().strip("Grade ") # (int 8-12)


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
    "Distractions in class. i.e. devices/people",
    "talking",
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
    "when": "When do you usually come in for support with studies?	What do you use flex block for?	",
    "what": "What prevents you most from using flex block to study/work on assignments?",
    "prevent": "How would you feel if flex time was removed?",
    "how": "Do you have any other comments or thoughts?"
}

df = clean_ms_forms_checkboxes(df, "when", when)
df = clean_ms_forms_checkboxes(df, "what", what)
df = clean_ms_forms_single(df, "prevent", prevent)

df.to_excel('filename.xlsx', index=False)
# df.to_csv('filename.csv', index=False, encoding="utf-8")


#------------------------

import matplotlib.pyplot as plt

# --- Ensure this goes AFTER your existing data cleaning code ---

# 1. Prepare data for columns containing lists (checkboxes)
# .explode() creates a separate row for each item in the list, allowing accurate value counts
df_when_exploded = df.explode('when')
df_what_exploded = df.explode('what')

# ==========================================
# PIE CHARTS
# ==========================================

# Pie Chart: Grade Distribution
plt.figure(figsize=(8, 6))
df['grade'].value_counts().plot.pie(autopct='%1.1f%%', startangle=140, cmap='Pastel1')
plt.title('Distribution of Students by Grade')
plt.ylabel('') # Hides the y-label for a cleaner look
plt.show()

# Pie Chart: What prevents students from using Flex block?
plt.figure(figsize=(10, 8))
df['prevent'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, cmap='Set3')
plt.title('What Prevents Students from Using Flex Block?')
plt.ylabel('')
plt.tight_layout()
plt.show()

# ==========================================
# BAR CHARTS (Multiple Choice/Checkboxes)
# ==========================================

# Horizontal Bar Chart: What is Flex block used for?
plt.figure(figsize=(10, 6))
df_what_exploded['what'].value_counts().sort_values().plot.barh(color='skyblue')
plt.title('What Students Use Flex Block For')
plt.xlabel('Number of Mentions')
plt.tight_layout()
plt.show()

# Bar Chart: When do students come in?
plt.figure(figsize=(8, 6))
df_when_exploded['when'].value_counts().plot.bar(color='lightgreen', rot=45)
plt.title('When Students Seek Support')
plt.ylabel('Number of Mentions')
plt.tight_layout()
plt.show()

# ==========================================
# COMPARISONS & CORRELATIONS
# ==========================================

# Comparison 1: Average 'Often' score by Grade
# Shows which grades utilize flex time the most on average
plt.figure(figsize=(8, 6))
df.groupby('grade')['often'].mean().sort_index().plot.bar(color='coral')
plt.title('Average Frequency of Flex Time Usage by Grade\n(1 = Never, 5 = Very Often)')
plt.xlabel('Grade')
plt.ylabel('Average Frequency Score')
plt.ylim(0, 5) # Lock scale to 1-5 range
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# Comparison 2: Stacked Bar - Prevention reasons broken down by Grade
# Shows if certain grades face specific barriers more than others
cross_tab_prevent = pd.crosstab(df['grade'], df['prevent'])
cross_tab_prevent.plot(kind='bar', stacked=True, figsize=(12, 8), cmap='tab20')
plt.title('Barriers to Using Flex Time by Grade')
plt.xlabel('Grade')
plt.ylabel('Number of Students')
plt.xticks(rotation=0)
plt.legend(title='Prevention Reason', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Comparison 3: Usage ('what') broken down by Grade
cross_tab_what = pd.crosstab(df_what_exploded['grade'], df_what_exploded['what'])
cross_tab_what.plot(kind='bar', figsize=(14, 8), cmap='Set2')
plt.title('Flex Time Activities by Grade')
plt.xlabel('Grade')
plt.ylabel('Number of Mentions')
plt.xticks(rotation=0)
plt.legend(title='Activity', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()