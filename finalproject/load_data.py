import json
import glob
import pandas as pd
from course import Course


def load_data(years):
    meta_data = {}
    info_data = {}
    data = {}

    for year in years:
        with open(f"./data/{year}/meta.json", "r", encoding="utf-8") as f:
            meta_data[year] = json.load(f)
        info_data[year] = {}
        for file_name in glob.glob("./data/" + year + "/json/*.json"):
            with open(file_name, "r", encoding="utf-8") as f:
                j = json.load(f)
                serial = j["serial"].lstrip("0")
                if serial == "":
                    serial = "0"
                info_data[year][serial] = j

        people_data = pd.read_csv(f"./data/{year}/people.csv")[
            ["開課序號", "選修人數", "全英語", "中文課程名稱"]
        ]

        data[year] = {}
        for course in meta_data[year]:
            serial = str(course["serial"])
            p_data = people_data[people_data["開課序號"] == int(serial)]

            if serial in info_data[year].keys() and course["type"] == "通":
                data[year][serial] = Course(course, info_data[year][serial], p_data)

    return data


# def load_data(years):
#     data_info = {}
#     people_data = {}
#     data = {}
#     for year in years:
#         with open(f"./data/{year}.json", "r", encoding="utf-8") as f:
#             data_info[year] = json.load(f)
#         people_data = pd.read_csv(f"./data/{year}/people.csv")[
#             ["開課序號", "選修人數", "全英語", "中文課程名稱"]
#         ]

#         for course in data_info[year]:
#             data[course["serial"]] = Course(course, people_data)
