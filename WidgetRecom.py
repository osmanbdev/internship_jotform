import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
import json
data=pd.read_csv('widgetdata.csv')


image = Image.open('jotform.png')
st.image(image, width = 500)
st.title('Widget Recommendation')
st.sidebar.header('Input Options')
st.subheader('JotForm Forms **Widget Recommendation Tool**')
st.markdown('**Widgets below might be useful**:')
# reading the data from the file
with open('SortedCategories.txt') as S:
    data1 = S.read()
 
# reconstructing the data as a list
categories = json.loads(data1)


# reading the data from the file
with open('SortedWidgetNames.txt') as w:
    data1 = w.read()
 
# reconstructing the data as a list
widget_names = json.loads(data1)
 
        
# reading the data from the file
with open('GlobalDict.txt') as d:
    data1 = d.read()
  
# reconstructing the data as a dictionary
globaldict = json.loads(data1)


# reading the data from the file
with open('GlobalList.txt') as l:
    data1 = l.read()
  
# reconstructing the data as a list
globallist = json.loads(data1)

# reading the data from the file
with open('FormCategory.txt') as c:
    data1 = c.read()
 
# reconstructing the data as a string
formcategory = json.loads(data1)


Selected_Widgets =st.sidebar.multiselect('Add a Widget', widget_names,key = 'multi')
Form_Category = st.sidebar.selectbox('Form Category', categories)
NumberOfWidgets = st.sidebar.slider('Number Of Widgets Shown', 1, 10, 5)



def onclickfunc(widget_name):
    st.session_state['multi'] = st.session_state['multi']+[widget_name]
    return   


def recomwidget(Widgets,Category):
    if len(set(Widgets).difference(set(globallist))) != 0:
        widget = list(set(Widgets).difference(set(globallist)))[0]
        globallist.append(widget)
        for i in range(0,data.shape[0]):
            if Category == 'All':
                if ((widget in data.widget_name[i].split(',')) and (len(data.widget_name[i].split(',')) > 1)):
                    for anotherstring in data.widget_name[i].split(','):
                        globaldict[anotherstring] = globaldict[anotherstring] + (anotherstring != widget)  
            elif Category == data['Form Category'][i]:
                if ((widget in data.widget_name[i].split(',')) and (len(data.widget_name[i].split(',')) > 1)):
                    for anotherstring in data.widget_name[i].split(','):
                        globaldict[anotherstring] = globaldict[anotherstring] + (anotherstring != widget)
    elif len(set(globallist).difference(set(Widgets))) != 0:
        widget = list(set(globallist).difference(set(Widgets)))[0]
        globallist.remove(widget)
        for i in range(0,data.shape[0]):
            if Category == 'All':
                if ((widget in data.widget_name[i].split(',')) and (len(data.widget_name[i].split(',')) > 1)):
                    for anotherstring in data.widget_name[i].split(','):
                        globaldict[anotherstring] = globaldict[anotherstring] - (anotherstring != widget)
            elif Category == data['Form Category'][i]:
                if ((widget in data.widget_name[i].split(',')) and (len(data.widget_name[i].split(',')) > 1)):
                    for anotherstring in data.widget_name[i].split(','):
                        globaldict[anotherstring] = globaldict[anotherstring] - (anotherstring != widget)
    

    return 
     

if Form_Category == formcategory:
    recomwidget(Selected_Widgets,Form_Category)
    with open('GlobalList.txt', 'w') as convert_file:
        convert_file.write(json.dumps(Selected_Widgets))
        
    with open('GlobalDict.txt', 'w') as convert_file:
        convert_file.write(json.dumps(globaldict))
        
else:
    
    globallist = []
    globaldict = {widget_names[i] : 0 for i in range(0,len(widget_names))}
    
    for i in range(0,len(Selected_Widgets)):
        recomwidget(Selected_Widgets,Form_Category)

    with open('GlobalList.txt', 'w') as convert_file:
        convert_file.write(json.dumps(Selected_Widgets))
        
    with open('GlobalDict.txt', 'w') as convert_file:
        convert_file.write(json.dumps(globaldict))

    with open('FormCategory.txt', 'w') as convert_file:
        convert_file.write(json.dumps(Form_Category))
        
newdict = {key: globaldict[key] for key in globaldict if key not in Selected_Widgets}
sorted_dict = sorted(newdict.items(),key = lambda x : x[1],reverse = True)

for i in range(0,NumberOfWidgets):
    
    st.button(sorted_dict[i][0],on_click = onclickfunc,kwargs={'widget_name':sorted_dict[i][0]})



#st.write({k: v for k, v in sorted(globaldict.items(), key=lambda item: item[1],reverse=True)})
#st.write(st.session_state)