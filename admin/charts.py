from matplotlib import pyplot as plt
import matplotlib
import io, base64
import numpy as np

__Colors = {
    "Natural Sciences": "#90BE6D",
    "Mathematics and Statistics": "#F9393C",
    "Engineering and Technology": "#206683",
    "Medical and Health Sciences": "#43AA8B",
    "Social Sciences": "#774304",
    "Humanities": "#F9C74F",
    "Arts and Design": "#552381",
    "Business and Management": "#B0D4D2",
    "Law and Legal Studies": "#FA9461",
    "Education": "#F3722C",
    "Computer Science and Information Systems": "#577590",
    "Environmental and Agricultural Sciences": "#2E4601",
    "Communication and Media": "#A975A6",
    "Interdisciplinary Studies": "#BBA0AE",
}

def __genImage():
    buffer = io.BytesIO()
    plt.savefig(buffer, format='svg', bbox_inches='tight')
    buffer.seek(0)
    plt.close()

    imagePNG = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(imagePNG)
    return graphic.decode('utf-8')

def usersPerInterest(data, city):
    matplotlib.use('Agg')
    fix, ax = plt.subplots()
    colors = plt.get_cmap('Blues')(np.linspace(0.4, 1, len(list(data.values()))))
    
    ax.pie(list(data.values()), labels=list(data.keys()), colors=[__Colors[label] for label in list(data.keys())], autopct='%1.1f%%',
            wedgeprops={"edgecolor": 'white', "linewidth": 1})

    plt.title(f"Users per Interest")
    plt.tight_layout()

    return __genImage()


def ageRangesPerInterest(data, city):
    matplotlib.use('Agg')
    #Formmated data:
    interests = list(data.keys())
    numInterests = len(interests)
    ageRanges = ['18-', '18-24', '25-34', '35-44', '45-54', '55+']
    numAges = len(ageRanges)

    values = [[data[interest][age] for age in ageRanges] for interest in interests]

    #Required for bar plotting
    x = np.arange(numAges) #Label locations
    barWidth = 0.25
    
    fix, ax = plt.subplots()
    for idx, (interest, val) in enumerate(zip(interests, values)):
        ax.bar(x + idx * barWidth, val, width = barWidth, label=interest, color=__Colors[interest])

    ax.set_title(f"User's Age Range per interest")
    ax.set_xlabel('Age Categories')
    ax.set_ylabel('Number of persons per interest')
    ax.set_xticks(x + barWidth * (numInterests - 1) / 2)
    ax.set_xticklabels(ageRanges)
    yMax = max([max(val) for val in values])
    ax.set_yticks(np.arange(0, yMax + 1, 1))
    ax.legend()

    return __genImage()