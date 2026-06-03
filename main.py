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
    "grade": "What Grade are you in?"
    "often": "How often do you utilize your flex block to receive help with homework?"
    "when": "When do you usually come in for support with studies?	What do you use flex block for?	"
    "what": "What prevents you most from using flex block to study/work on assignments?"
    "prevent": "How would you feel if flex time was removed?"
    "how": "Do you have any other comments or thoughts?"
}

df = clean_ms_forms_checkboxes(df, "when", when)
df = clean_ms_forms_checkboxes(df, "what", what)
df = clean_ms_forms_single(df, "prevent", prevent)

df.to_excel('filename.xlsx', index=False)
# df.to_csv('filename.csv', index=False, encoding="utf-8")


#------------------------