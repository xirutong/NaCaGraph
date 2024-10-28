import matplotlib.pyplot as plt
import json
import pylab as mpl

def getcontent(filepath):
    with open(filepath, 'r',encoding='utf-8-sig') as f:
        content=json.load(f)
    f.close()
    return content

#Converts downloaded data into image data:
# blank years are supplemented with 0, blank topics are supplemented with a list of all zeros.
def data_processing(dic,topics_list):
    the_dict={}
    for i in dic:
        topic=i["Topic"]
        year=i["Year"]
        numt=i["num_trigger"]
        if topic in the_dict:
            the_dict[topic]["year"].append(year)
            the_dict[topic]["numt"].append(numt)
        else:
            the_dict[topic]={}
            the_dict[topic]["year"]=[]
            the_dict[topic]["numt"] = []
            the_dict[topic]["year"].append(year)
            the_dict[topic]["numt"].append(numt)
    year=list(range(2023,2004,-1))
    zero_list=[0 for _ in range(len(year))]
    for t in topics_list:
        if t not in the_dict.keys():
            the_dict[t]={}
            the_dict[t]["year"]=year
            the_dict[t]["numt"]=zero_list
        else:
            for j in range(2023,2004,-1):
                num=year.index(j)
                if num>=len(the_dict[t]["year"]) or the_dict[t]["year"][num]<j :
                    the_dict[t]["year"].insert(num, j)
                    the_dict[t]["numt"].insert(num, 0)
    for i in the_dict:
        if the_dict[i]["year"][-1]!=2004:
            the_dict[i]["year"].append(2004)
            the_dict[i]["numt"].append(0)
    return the_dict

#check the data
def print_dict(the_dict):
    # #get data
    year = list(range(2023, 2004, -1))
    verts=[]
    for i in the_dict:
        vert = []
        print('-------topic:',i,'-----------')
        print(the_dict[i]["year"],len(the_dict[i]["year"]))
        print(the_dict[i]["numt"],len(the_dict[i]["numt"]))
        #topics_list.append(i)
        for k in range(len(year)):
            temp = (the_dict[i]["year"][k], the_dict[i]["numt"][k])
            vert.append(temp)
        print(vert)
        verts.append(vert)
    for i in verts:
        print(i)

#draw
def draw_3d(topics_list,the_dict):
    mpl.rcParams['font.sans-serif'] = ['FangSong']
    mpl.rcParams['axes.unicode_minus'] = False
    fig = plt.figure(figsize = (10,8))
    ax = fig.add_subplot(111, projection='3d')
    xs = list(range(2023,2003,-1))

    for y in range(len(topics_list)):
        zs = the_dict[topics_list[y]]["numt"]
        ax.plot(xs, zs, zs=y, zdir='y', marker='o',markersize=4 ,alpha=0.8)
    # In the case of setting zdir = 'y', the y-axis is actually the z-axis, and then the z-axis becomes the y-axis
    ax.set_xlabel('Years',labelpad=13.5)
    ax.set_ylabel('Topics',labelpad=13.5)
    ax.set_zlabel('Num of trigger "fire"',labelpad=5.5)

    print(len(topics_list))
    ax.set_xlim3d(2004,2023)
    ax.set_ylim3d(0,len(topics_list))
    ax.set_zlim3d(0,30)
    ax.set_xticks(list(range(2023,2003,-1)))

    print(topics_list)
    ax.set_yticklabels(topics_list)
    ax.set_box_aspect([10, 10, 3])
    plt.tick_params(axis='x', labelsize=8)
    plt.show()


filepath="records_4topic_fire.json"
dic=getcontent(filepath)
topics_list=['climate_change', 'greenhouse','earthquake','high_temperature',  'drought', 'forest_fire',  'wildfire']
the_dict=data_processing(dic,topics_list)
#print_dict(the_dict)
draw_3d(topics_list,the_dict)