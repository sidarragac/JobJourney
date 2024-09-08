from matplotlib import pyplot as plt
import io, base64
import numpy as np

def __genImage():
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    imagePNG = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(imagePNG)
    return graphic.decode('utf-8')

def usersPerInterest(data, city):
    fix, ax = plt.subplots()
    colors = plt.get_cmap('Blues')(np.linspace(0, 1, len(list(data.values()))))
    
    ax.pie(list(data.values()), labels=list(data.keys()), colors=colors, autopct='%1.1f%%',
            wedgeprops={"edgecolor": 'white', "linewidth": 1})

    plt.title(f"Users per Interest in {city} ")

    return __genImage()


def ageRangesPerInterest(data, city):
    #Formmated data:
    interests = list(data.keys())
    numInterests = len(interests)
    ageRanges = ['U18', '18-30', '30-50', 'O50']
    numAges = len(ageRanges)

    values = [[data[interest][age] for age in ageRanges] for interest in interests]

    #Required for bar plotting
    x = np.arange(numAges) #Label locations
    barWidth = 0.25
    
    fix, ax = plt.subplots()
    for idx, (interest, val) in enumerate(zip(interests, values)):
        ax.bar(x + idx * barWidth, val, width = barWidth, label=interest)

    plt.title(f"User's Age Range per interest in {city}")
    ax.set_xlabel('Age Categories')
    ax.set_ylabel('Values')
    ax.set_title('Grouped Bar Chart')
    ax.set_xticks(x + barWidth * (numInterests - 1) / 2)
    ax.set_xticklabels(ageRanges)
    ax.legend()

    return __genImage()