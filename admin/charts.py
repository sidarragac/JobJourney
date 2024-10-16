import io
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set Seaborn style
sns.set_theme(context='notebook', style="whitegrid")

def __genImage():
    buffer = io.BytesIO()
    plt.savefig(buffer, format='svg', bbox_inches='tight')
    buffer.seek(0)
    plt.close()

    imageSVG = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(imageSVG)
    return graphic.decode('utf-8')

def usersPerInterest(data, colors):
    interests = list(data.keys())
    numberOfUsers = list(data.values())

    plt.figure(figsize=(10, 10))
    plt.pie(numberOfUsers, labels=interests, colors=[colors[interest] for interest in interests], 
            autopct='%1.1f%%', wedgeprops={"edgecolor": 'white', "linewidth": 1}, startangle=140, textprops={'fontsize': 16, 'weight': 'bold'})

    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    plt.title("Users per Interest", fontsize=18, weight='bold', loc='left')
    plt.tight_layout()

    return __genImage()

def ageRangesPerInterest(data, colors):
    #Formmated data:
    interests = list(data.keys())
    numInterests = len(interests)
    ageRanges = ['18-', '18-24', '25-34', '35-44', '45-54', '55+']
    numAges = len(ageRanges)

    values = [[data[interest][age] for age in ageRanges] for interest in interests]

    #Required for bar plotting
    x = np.arange(numAges) #Label locations
    barWidth = 0.25
    
    fig, ax = plt.subplots(figsize=(10, 10))
    for idx, (interest, val) in enumerate(zip(interests, values)):
        ax.bar(x + idx * barWidth, val, width = barWidth, label=interest, color=colors[interest])

    ax.set_title(f"User's Age Range per interest", fontsize=16, weight='bold', loc='left')
    ax.set_xlabel('Age Categories', fontsize=14, weight='bold')
    ax.set_ylabel('Number of persons per interest', fontsize=14, weight='bold')
    ax.set_xticks(x + barWidth * (numInterests - 1) / 2)
    ax.set_xticklabels(ageRanges, fontsize=14)
    yMax = max([max(val) for val in values])
    ax.tick_params(axis='y', labelsize=14)
    ax.set_yticks(np.arange(0, yMax + 1, 1))
    ax.legend(title='Interests', bbox_to_anchor=(1.05, 1), loc='upper left')

    return __genImage()

def roadmapCompletionPercentage(data, colors):
    #Data Preparation to plot
    interests = []
    completionPercentages = []
    colorList = []
    for interest, percentages in data.items():
        for pct in percentages:
            interests.append(interest)
            completionPercentages.append(pct)
            colorList.append(colors[interest])

    plt.figure(figsize=(8, 6))
    sns.stripplot(x=interests, y=completionPercentages, hue=interests, legend=False, palette=colors, jitter=True, dodge=True)

    plt.title("Roadmap Completion Percentage by Interest", fontsize=16, weight='bold', loc='left')
    plt.xlabel('Interest', fontsize=14, weight='bold')
    plt.ylabel('Completion Percentage', fontsize=14, weight='bold')
    plt.tight_layout()

    return __genImage()