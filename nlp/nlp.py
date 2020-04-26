import nltk
import csv
from nltk.tokenize import word_tokenize, sent_tokenize
#from nltk.stem import PorterStemmer
global_series_tolerance = 8
global_number_tolerance = 4


agewords = ['yo', 'years', 'year','old', 'aged', 'age', 'yr','yrs']
genderwords = ['male', 'man','boy','woman','female','girl']
identifier = ['mr', 'ms', 'mrs']
bmi_list = ['body','mass','index', 'bmi', 'kg/m2', 'kg/m']
bp_list = ['systolic', 'diastolic', 'pressure', 'blood-pressure', 'bp']
temp_list = ['temperature', 'temp','body-temp']
hdl_list = ['hdl', 'high-density-lipid']
ldl_list = ['ldl', 'low-density-lipid']
vldl_list = ['vldl','very-low-density-lipid','lipoprotien']
a1c_list = ['a1c','glycohemoglobin','hba1c','glycated-hemoglobin',' glycated hemoglobin','glycated']
crp_list = ['crp', 'c-reactive','reactive-protien']
pulse_list = ['pulse', 'heart-rate']
platelet_list = ['platelet', 'platelets']
aso_list = ['aso', 'Antistreptolysin', 'Antistreptolysin O Titre']
esr_list = ['esr', 'erythrocyte', 'sediment', 'rate']
bleedingtime_list = ['bleedingtime', 'bt']
clottingtime_list = ['clotting-time', 'clotting','ct']
prothombin_list = ['prothrombin-time', 'prothrombin','pt']
aptt_list = ['aptt', 'ptt', 'activated-partial-thromboplastin-time', 'partial-thromboplastin-time']
wbc_list = ['wbc', 'wiite-blood-cell']
rbc_list = ['rbc', 'red-blood-cell', 'red-blood-cells']
bloodUreaNitrogen_list = ['bun-level, blood-urea-nitrogen','urea-nitrogen']
creatinine_list = ['creatinine']
sodium_list = ['sodium']
potassium_list = ['potassium']
phosphate_list = ['phosphate']
magnesium_list= ['magnesium']
amylase_list = ['amylase']
lipase_list = ['lipase']
tsh_list = ['tsh', 'thyroid', 'simulating', 'hormone']
uricacid_list = ['uric', 'acid']
troponin_t_list = ['troponin-t','troponin']
troponon_i_list = ['troponon-i','troponin']
ldh_list = ['ldh','lactic','acid', 'dehydrogena se']
triglycerides_list = ['triglycerides']
disease_list = ['history','medical', 'diagnosed', 'reported','identified','treated','suffered','suffering']
medications_list =['taking', 'prescribed','medications-include',' medicament','pills',
                    'oinments','oinment','pill','pills','medicaments','elixir','balm',
                    'inoculation','potion','potions','remedy','remedies','prescription','serum','tablet','tablets']

symptoms_list = ['suffered','suffering-from','reports-of','reports','experiencing','experiences','experienced','affected','endure','feeling','feels']


openfileloc =r"C:\Users\boomr\OneDrive\Desktop\nlp\output.txt"
outputfileloc =r"C:\Users\boomr\OneDrive\Desktop\nlp"
file = open(openfileloc, "r")
bulkdata = file.read()
file.close()
dataset = [("--start-- "+i+" -"*(global_series_tolerance+2)+"end") for i in bulkdata.split("\n\n")]

class data_collect:
    def __init__(self):
        self.values = {}
        self.raw = {}

    def add(self, key, val):
        self.values[key] = val

    def raw_ip(self, key, val):
        self.raw[key] = val


def fetch_details(text, options = 1, write = 0):

    sentences = sent_tokenize(text)
    wordsInSent1 = word_tokenize(sentences[0])
    sent1_pos = nltk.pos_tag(wordsInSent1)
    details = data_collect()

    r = [x[0] for x in sent1_pos if x[1] == 'NNP']

    name = [r[i]+" "+r[i+1] for i in range(len(r)-1) if any(word in r[i].lower() for word in identifier)]+r
    details.add('NAME                                       					: ', name[0])
    details.raw_ip('NAME',name)

    age = search_age(wordsInSent1)
    details.add('AGE                                          					: ', age[0])
    details.raw_ip('Age', age)

    gender = [i for i in wordsInSent1 if i.lower() in genderwords]+['N/A']
    details.add('GENDER                                     					: ', gender[0])
    details.raw_ip('Gender', gender)


    wordsInText = [x.lower() for x in word_tokenize(text)]

    bmi = search_around(bmi_list, wordsInText,2)
    details.add('BMI 				[18.5 - 24.9]			: ', bmi[0])
    details.raw_ip('BMI', bmi)

    bloodpressure = search_around(bp_list, wordsInText, 5)
    if bloodpressure[0] == 'N/A':
        bp = bloodpressure
    else:
        bp = [x for x in bloodpressure[0].split('/')]
        if (len(bloodpressure)>1)|(len(bp)>=1):
            bp+=bloodpressure[1:]+['']
            bp = [bp[0]+'/'+bp[1]]
    details.add('BLOOD PRESSURE			[120 - 140 / 80-90]		: ', bp[0])
    details.raw_ip('Pressure', bp)

    temperature = search_specific(temp_list,wordsInText, 4)
    details.add('TEMPERATURE			[97 - 99 deg F]			: ', temperature[0])
    details.raw_ip('temperature', temperature)

    hdl = search_around(hdl_list, wordsInText, 3)
    details.add('HDL				[40 - 59 mg/dL]			: ', hdl[0])
    details.raw_ip('HDL', hdl)

    ldl = search_around(ldl_list, wordsInText, 3)
    details.add('LDL				[100 - 129 mg/dL]			: ', ldl[0])
    details.raw_ip('LDL', ldl)

    vldl = search_around(vldl_list,wordsInText, 3)
    details.add('VLDL				[2 - 30 mg/dL]			: ', vldl[0])
    details.raw_ip('VLDL', vldl)

    a1c = search_specific(a1c_list, wordsInText, 10)
    details.add('HbA1c				[4 - 5.6 %]			: ', a1c[0])
    details.raw_ip('HbA1c', a1c)

    crp = search_specific(crp_list, wordsInText, 4)
    details.add('C-REACTIVE PROTIEN		[0 - 1.0 mg/L]			: ', crp[0])
    details.raw_ip('CRP', crp)

    pulse = search_specific(pulse_list, wordsInText,4)
    details.add('PULSE				[60 - 100 bpm]			: ', pulse[0])
    details.raw_ip('Pulse', pulse)

    platelet = search_around(platelet_list, wordsInText, 2)
    details.add('PLATELET	COUNT			[150,000 - 450,000]		: ', platelet[0])
    details.raw_ip('platelets', platelet)

    aso = search_around('aso_list', wordsInText, 2)
    details.add('ANTISTREPTOLYSIN			[>200 units/mL]			: ', aso[0])
    details.raw_ip('ASO', aso)

    esr = search_series(esr_list,wordsInText, 2)
    details.add('ESR				[M (0 - 22) F (0 - 22) mm/hr]		: ',esr[0])
    details.raw_ip('ESR', esr)

    bleedingtime = search_specific(bleedingtime_list, wordsInText,4)
    details.add('BLEEDING TIME			[2 - 7 minutes]			: ', bleedingtime[0])
    details.raw_ip('Bleeding time', bleedingtime)

    clottingtime = search_specific(clottingtime_list, wordsInText, 6)
    details.add('CLOTTING TIME			[8 - 15 minutes]			: ', clottingtime[0])
    details.raw_ip('clottingtime', clottingtime)

    prothrombin = search_specific(prothombin_list, wordsInText, 5)
    details.add('PROTHROMBIN TIME		[9.5 - 13.5 seconds]		: ', prothrombin[0])
    details.raw_ip('prothrombin', prothrombin)

    wbc = search_specific(wbc_list, wordsInText, 4)
    details.add('WBC				[4500 - 11000 per µL]		: ', wbc[0])
    details.raw_ip('WBC', wbc)

    rbc = search_specific(rbc_list, wordsInText, 4)
    details.add('RBC				[M (4.7 - 6.1) F (4.2 - 5.4) mcL]	: ', rbc[0])
    details.raw_ip('RBC', rbc)

    bloodUreaNitrogen = search_specific(bloodUreaNitrogen_list, wordsInText, 5)
    details.add('BLOOD UREA NITROGEN		[7 - 20 mg/dL]			: ', bloodUreaNitrogen[0])
    details.raw_ip('bloodUreaNitrogen', bloodUreaNitrogen)

    creatinine = search_specific(creatinine_list, wordsInText, 5)
    details.add('CREATININE			[M (0.6 - 1.2 ) F (0.5 - 1.1) mg/dL]	: ' , creatinine[0])
    details.raw_ip('CREATININE', creatinine)

    sodium = search_specific(sodium_list, wordsInText, 4)
    details.add('SERUM (SODIUM)			[134 - 145 mEq/L]			: ',sodium[0])
    details.raw_ip('Serum sodium', sodium)

    potassium = search_specific(potassium_list, wordsInText, 4)
    details.add('SERUM (POTASSIUM)        		[3.5 - 5.0 mmol/L]    		: ', potassium[0])
    details.raw_ip('potassium', potassium)

    magnesium = search_specific(magnesium_list, wordsInText, 4)
    details.add('SERUM (MAGNESIUM)        		[0.70 - 0.95 mmol/L]  		: ', magnesium[0])
    details.raw_ip('magnesium', magnesium)

    phosphate = search_specific(phosphate_list, wordsInText, 4)
    details.add('SERUM (PHOSPHATE)       		[0.8 - 1.3 mmol/L]			: ', phosphate[0])
    details.raw_ip('phosphate', phosphate)

    amylase = search_specific(amylase_list,wordsInText, 4)
    details.add('AMYLASE				[23 - 100 U/L]			: ',amylase[0])
    details.raw_ip('Amylase', amylase)

    lipase = search_specific(lipase_list,wordsInText, 4)
    details.add('LIPASE				[0 - 160 U/L]			: ',lipase[0])
    details.raw_ip('Lipase', lipase)

    tsh = search_specific(tsh_list, wordsInText,4)
    details.add('THYROID SIMULATING HORMONE	[0.4 - 4.0 mu/L]			: ',tsh[0])
    details.raw_ip('TSH', tsh)

    uricacid = search_specific(uricacid_list, wordsInText, 5)
    details.add('URIC ACID LEVEL			[M (2.4 - 6.0) F(3.4 - 7.0) mg/dL]	: ', uricacid[0])
    details.raw_ip('uricacid', uricacid)

    troponin_T = search_around(troponin_t_list, wordsInText, 3)
    details.add('TROPONIN - T			[M (0 - 10) F (0 - 15) ng/L]		: ', troponin_T[0])
    details.raw_ip('troponin_T', troponin_T)

    troponin_I = search_around(troponon_i_list, wordsInText, 3)
    details.add('TROPONIN - I			[M (0 - 10) F (0 - 10) ng/L]		: ', troponin_I[0])
    details.raw_ip('troponin_I', troponin_I)

    ldh = search_around(ldh_list, wordsInText,5)
    details.add("LACTIC ACID DEHYDROGENASE	[100 - 190 units/L]    	 	: " ,ldh[0])
    details.raw_ip('LDH', ldh)

    triglycerides = search_specific(triglycerides_list, wordsInText,5)
    details.add("TRIGLYCERIDES			[0 - 150 mg/dL]     	        		: ", triglycerides[0])
    details.raw_ip('triglycerides', triglycerides)

    disease = search_after_sym(disease_list,wordsInText,3)
    details.add("DISEASES                                  					: ",disease)
    details.raw_ip("disease",disease)

    symptoms = search_after_sym(symptoms_list, wordsInText,3)
    details.add("SYMPTOMS                                					: ", symptoms)
    details.raw_ip("symptopms", symptoms)

    medications = search_after_sym(medications_list, wordsInText,3)
    details.add("MEDICATIONS                             					: ", medications)
    details.raw_ip("medications",medications)

    if write==1:
        with open(r'C:\Users\boomr\OneDrive\Desktop\nlp\nlp.csv','w') as f:
            w = csv.writer(f)
            w.writerows(details.values.items())
    if write == 2:
        with open(outputfileloc + 'details_raw.csv','w') as f:
            w = csv.writer(f)
            w.writerows(details.raw.items())

    if options == 0:
        return details

    if options == 1:
        for i in details.values.keys():
            print("{}\t:{}".format(i, details.values[i]))
        print()
    if options == 2:
        for i in details.raw.keys():
            print("{}\t:{}".format(i, details.raw[i]))
        print()

def search_age(sent):
    numbers = [data for data in sent if any([e.isnumeric() for e in data])]
    agestr = isage(numbers)
    age = [extractNumeric(i) for i in agestr]
    age = [t for t in age if int(t)<110]+['N/A']
    return age

def extractNumeric(s):
    p, index, prev = [], -1, False
    t = [(i, i.isnumeric()) for i in s]
    for i in t:
        if i[1]:
            if not prev:
                p.append(i[0])
                index+=1
            else:
                p[index]+=i[0]
        prev = i[1]
    p.append('')
    return p[0]


def isage(strList):
    finalAgeStr = [i for i in strList if any(word in i.lower() for word in agewords)]
    finalAgeStr += [i for i in strList if i.isnumeric()]
    return finalAgeStr


def search_around(key_list,words_list, tolerance, depth = 2):
    tolerance = min(global_number_tolerance, tolerance)
    depth = min(5,depth)
    found = []
    flag, f_index = 1,-1
    for word in words_list:
        if word.lower() in key_list:
            f_index =  words_list.index(word)
            break
    if f_index == -1:
        return ['N/A']
    index = f_index
    while flag:
        for i in range(index+1, index+2+tolerance):
            if words_list[i].lower() in key_list:
                index = i
                continue
        flag = 0
    for i in range(f_index, index+depth+tolerance):
        if any([r.isnumeric() for r in words_list[i]]):
            found.append(words_list[i])
            li = i
    if len(found)>0:
        found.append(words_list[li+1])
        return found
    else:
        return ['N/A']

def search_specific(key_list, words_list,max_tolerance):
    max_tolerance= min(max_tolerance, global_series_tolerance-1)
    index = -1
    for element in words_list:
        if element.lower() in key_list:
            index = words_list.index(element)
            break
    if index!=-1:
        for i in range(index+1, index+1+max_tolerance):
            if any([r.isnumeric() for r in words_list[i]]):
                return [words_list[i], words_list[i+1]]
    return ['N/A']



def search_series(keylist, words_list, search_tolerance):
    search_tolerance = min(3, abs(search_tolerance))
    found = []
    index, keyindex = -1,0
    for i in range(len(keylist)):
        if keylist[i] in words_list:
            index = words_list.index(keylist[i])
            keyindex = i
            break
    flag = -len(keylist)+ keyindex+1
    if index == -1:
        return ['N/A']
    else:
        while flag:
            flag+=1
            keyindex += 1
            for i in range(index+1, index+2+search_tolerance):
                if any([r.isnumeric() for r in words_list[i]]):
                    found.append(words_list[i])
                    break
                if keylist[keyindex] in words_list[i]:
                    continue
    return (found+['N/A'])

def search_after_sym(keylist, words_list, search_tolerance):
    search_tolerance = min(3, abs(search_tolerance))
    found = []
    for word in words_list:
        if word in keylist:
            for i in range(words_list.index(word)+1,words_list.index(word)+search_tolerance+1):
                if(nltk.pos_tag([words_list[i]])[0][1] in ['NNP','NN','NNS']):
                    if(words_list[i] not in keylist):
                        found.append(words_list[i])
    found.append("Not Specified")

    return found

for i in dataset:

    details = fetch_details(i,options = 0, write = 1)

    for i in details.values.keys():
        print("{}\t:{}".format(i, details.values[i]))

input("Press enter to exit")
