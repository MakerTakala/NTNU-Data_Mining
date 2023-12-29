from apriori_python import apriori


def preprocess_data(courses):
    datas = []
    for course in courses.values():
        data = []
        data.append(course.name)
        for teacher in course.teachers:
            data.append(teacher)
        for domain in course.gu_domain:
            data.append(domain)
        for method in course.methods:
            data.append(method[0])
        for evaluation in course.evaluations:
            data.append(evaluation[0])
        choose = course.people / course.quota_limit + course.quota_additional
        if choose >= 0.9:
            data.append("選課率高")
        elif choose >= 0.7:
            data.append("選課率中")
        elif choose >= 0.5:
            data.append("選課率低")
        else:
            data.append("開課失敗")
        data.append("上課星期" + str(course.day))
        for i in range(course.time_from, course.time_to):
            data.append("上課時間" + str(i))
        data.append("上課地點" + str(course.campus))
        if course.emi:
            data.append("全英授課")
        for program in course.program:
            data.append("學程" + str(program))

        datas.append(data)
    return datas


def associate(courses):
    datas = preprocess_data(courses)
    association_rules = apriori(datas, minSup=0.76, minConf=0.9)
    # print(association_rules)
    association_rules = association_rules[1]

    doamins = ["人文藝術", "社會科學", "自然科學", "邏輯運算", "大學入門", "跨域專業探索課程", "學院共同課程", "專題探究"]

    use_in_domain = False

    print("association_rules:")
    for rule in association_rules:
        if use_in_domain:
            having = False
            for domain in doamins:
                if domain in rule[0] or domain in rule[1]:
                    having = True
                    break
            if having:
                print(rule)
        else:
            print(rule)
    print()
