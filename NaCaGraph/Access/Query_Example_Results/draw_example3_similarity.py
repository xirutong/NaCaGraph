import matplotlib.pyplot as plt
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def getcontent(filepath):
    with open(filepath, 'r',encoding='utf-8-sig') as f:
        content=json.load(f)
    f.close()
    return content

#Converting data into one-hot coding
def data_processing(dict,thestr,thestr2): #thestr: 'event_types' or "triggers" #thestr2: 'num_event_types' or "num_triggers"
    # Record all elements
    events_list=[]
    for i in dict:
        print(i)
        events=i[thestr]
        for e in events:
            if e not in events_list:
                events_list.append(e)
    # Arranged in the order of the topic list:
    topics_list=['climate_change', 'greenhouse','earthquake','high_temperature',  'drought', 'forest_fire',  'wildfire']
    dic=[]
    for i in topics_list:
        for j in dict:
            if j["topic"] ==i:
                dic.append(j)
                break
    print('_')
    print(dic)
    #Converting elements to one-hot coding of each topic
    data_list={}
    for i in dic:
        print(i)
        t=i["topic"]
        data_list[t]=[0 for _ in range(len(events_list))]
        events=i[thestr]
        for e in range(len(events)):
            eindex=events_list.index(events[e])
            data_list[t][eindex]= i[thestr2][e]  #'num_event_types' or "num_triggers"
    print('#')
    print(data_list)
    return data_list


def calculate_similarity(data_list):
    data = data_list
    # Convert the data dictionary to a matrix
    matrix = np.array(list(data.values()))
    # Calculate cosine similarity matrix
    similarity_matrix = cosine_similarity(matrix)
    # Print the similarity matrix
    print("similarity_matrix:")
    print(similarity_matrix)
    return similarity_matrix


def draw_similarity(similarity_matrix,data,titlename):
    # plt.figure(figsize = (7,8))
    # plt.imshow(similarity_matrix, cmap='hot', interpolation='nearest')
    # # Set the labels for x and y axes
    # plt.xticks(range(len(data)), list(data.keys()), rotation=90)
    # plt.yticks(range(len(data)), list(data.keys()))
    # # Add colorbar
    # plt.colorbar()
    # # Display the plot
    # plt.show()


    # Create a figure and axis
    fig, ax = plt.subplots()
    # Create x-axis ticks and labels
    x = np.arange(len(similarity_matrix))
    labels = list(data.keys())
    # Plot the similarity values as dotted lines
    for i in range(len(similarity_matrix)):
        y = similarity_matrix[i]
        ax.plot(x, y, linestyle=':', marker='o', label=labels[i])

    # Set the x-axis ticks and labels
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=30, ha='right')
    # Set the y-axis label
    ax.set_ylabel('Similarity')
    # Set the title
    ax.set_title(titlename)
    # Add a legend
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    # Display the plot
    plt.tight_layout()
    plt.show()

#pic1:  ten number of event types
filepath= "example3_eventtype.json"
thestr='event_types'
thestr2='num_event_types'#
titlename='Similarity between 7 Topic - with Event_type datas'
dict=getcontent(filepath)
data_list=data_processing(dict,thestr,thestr2)
similarity_matrix=calculate_similarity(data_list)
draw_similarity(similarity_matrix,data_list,titlename)

#pic2:  ten number of triggers
filepath="example3_trigger.json"
thestr="triggers"
thestr2="num_triggers"
titlename='Similarity between 7 Topic - with Trigger datas'

dict=getcontent(filepath)
data_list=data_processing(dict,thestr,thestr2)
similarity_matrix=calculate_similarity(data_list)
draw_similarity(similarity_matrix,data_list,titlename)
