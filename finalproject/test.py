from apriori_python import apriori

itemSetList = [
    ["eggs", "bacon", "soup"],
    ["eggs", "bacon", "apple"],
    ["soup", "bacon", "banana"],
]
freqItemSet, rules = apriori(itemSetList, minSup=0.5, minConf=0.5)
print(rules)
