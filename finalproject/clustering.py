from transformers import BertTokenizer
import numpy as np
from sklearn.cluster import KMeans


def preprocess_data(courses):
    tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
    doamins = ["人文藝術", "社會科學", "自然科學", "邏輯運算", "大學入門", "跨域專業探索課程", "學院共同課程", "專題探究"]
    ans = []
    datas = []
    for course in courses.values():
        data = []
        ans.append(doamins.index(course.gu_domain[-1]))
        teacher_encoder = []
        for teacher in course.teachers:
            name = np.mean(tokenizer.encode(teacher, add_special_tokens=False))
            teacher_encoder.append(name)
        data.append(np.mean(teacher_encoder))


def kmeans_clustering(data):
    preprocess_data(data)
