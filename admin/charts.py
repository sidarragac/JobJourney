from matplotlib import pyplot as plt
import matplotlib
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
    matplotlib.use('Agg')
    fix, ax = plt.subplots()
    colors = plt.get_cmap('Blues')(np.linspace(0.4, 1, len(list(data.values()))))
    
    ax.pie(list(data.values()), labels=list(data.keys()), colors=colors, autopct='%1.1f%%',
            wedgeprops={"edgecolor": 'white', "linewidth": 1})

    plt.title(f"Users per Interest in {city} ")


    return __genImage()


def ageRangesPerInterest(data, city):
    matplotlib.use('Agg')
    #Formmated data:
    interests = list(data.keys())
    numInterests = len(interests)
    ageRanges = ['-18', '18-30', '30-50', '+50']
    numAges = len(ageRanges)

    values = [[data[interest][age] for age in ageRanges] for interest in interests]

    #Required for bar plotting
    x = np.arange(numAges) #Label locations
    barWidth = 0.25
    
    fix, ax = plt.subplots()
    for idx, (interest, val) in enumerate(zip(interests, values)):
        ax.bar(x + idx * barWidth, val, width = barWidth, label=interest)

    ax.set_title(f"User's Age Range per interest in {city}")
    ax.set_xlabel('Age Categories')
    ax.set_ylabel('Number of persons per interest')
    ax.set_xticks(x + barWidth * (numInterests - 1) / 2)
    ax.set_xticklabels(ageRanges)
    yMax = max([max(val) for val in values])
    ax.set_yticks(np.arange(0, yMax + 1, 1))
    ax.legend()

    return __genImage()