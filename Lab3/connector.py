import pandas as pd

def write_excel(filename,sheetname,dataframe):
    with pd.ExcelWriter(filename, engine='openpyxl', mode='a') as writer: 
        workBook = writer.book
        try:
            workBook.remove(workBook[sheetname])
        except:
            print("Worksheet does not exist")
        finally:
            dataframe.to_excel(writer, sheet_name=sheetname)
            writer._save()

with open(r'C:\Users\GreenDe\Desktop\VUZ\PIS (LABA)\Lab3\out.txt', 'r') as inputfile:
    data = inputfile.readlines()
    
for i, piece in enumerate(data):
    data[i].replace('\n', '')
    data[i] = piece.split(' ')
    
newdata = {}
for buy in data:
    if buy[1] not in newdata.keys():
        newdata[buy[1]] = 0
    newdata[buy[1]] += int(buy[2]) * int(buy[3]) - int(buy[2]) * int(buy[4])
    #newdata.update({buy[1]:})
   #try:
   #    strippeddata.update({buy[1]:round((strippeddata[buy[1]] + float(buy[5])),2)})
   #except:
   #    strippeddata.update({buy[1]:0})
   #    strippeddata.update({buy[1]:round((strippeddata[buy[1]] + float(buy[4]) - float(buy[5])),2)})

#print(strippeddata)
mydataframe = pd.Series(newdata)
print(mydataframe)
#mydataframe.to_frame(name='bruh')
#print(mydataframe)
writer = pd.ExcelWriter(r'C:\Users\GreenDe\Desktop\VUZ\PIS (LABA)\Lab3\out.xlsx', mode='a', if_sheet_exists='overlay')
write_excel(r'C:\Users\GreenDe\Desktop\VUZ\PIS (LABA)\Lab3\out.xlsx', 'Sheet1', mydataframe)
