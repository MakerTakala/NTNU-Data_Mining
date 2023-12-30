from transformers import BertTokenizer
import numpy as np
from scipy.stats import entropy
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN

MAX_TOEKN_SIZE = 30522


def preprocess_data(courses):
    tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
    domains = ["人文藝術", "社會科學", "自然科學", "邏輯運算", "大學入門"]
    programs = []

    for course in courses.values():
        for program in course.program:
            if program not in programs:
                programs.append(program)

    ans = []
    datas = []
    for course in courses.values():
        data = []
        ans_flag = False
        for i, domain in enumerate(domains):
            if course.gu_domain[0] == domain:
                ans.append(i)
                ans_flag = True

        if not ans_flag:
            continue

        name_encoder = [0] * MAX_TOEKN_SIZE
        for text in course.name:
            token = tokenizer.encode(text, add_special_tokens=False)
            if token != []:
                name_encoder[token[0]] += 1

        description_encoder = [0] * MAX_TOEKN_SIZE
        for text in course.description:
            token = tokenizer.encode(text, add_special_tokens=False)
            if token != []:
                description_encoder[token[0]] += 1

        for program in programs:
            if program in course.program:
                data.append(1)
            else:
                data.append(0)

        datas.append(data + name_encoder + description_encoder)
    min_max_scaler = MinMaxScaler()
    datas = min_max_scaler.fit_transform(datas)

    return datas, ans


def score_entropy(labels, anss, real_classes, label_classes):
    clusters = [[] for _ in range(label_classes)]
    clusters_prob = [0] * label_classes
    for label, ans in zip(labels, anss):
        if label == -1:
            continue
        clusters[label].append(ans)
        clusters_prob[label] += 1
    clusters_prob = np.array(clusters_prob) / len(labels)

    score = 0
    for index, cluster in enumerate(clusters):
        lab = [0] * real_classes
        for tag in cluster:
            lab[tag] += 1
        for i in range(real_classes):
            if lab[i] == 0:
                continue
            lab[i] = lab[i] / len(cluster)
        # remove 0 in lab
        lab = [i for i in lab if i != 0]
        score += entropy(lab) * clusters_prob[index]

    return score


def score_purity(labels, anss, real_classes, label_classes):
    clusters = [[] for _ in range(label_classes)]
    clusters_prob = [0] * label_classes
    for label, ans in zip(labels, anss):
        if label == -1:
            continue
        clusters[label].append(ans)
        clusters_prob[label] += 1
    clusters_prob = np.array(clusters_prob) / len(labels)

    score = 0
    for index, cluster in enumerate(clusters):
        lab = [0] * real_classes
        for tag in cluster:
            lab[tag] += 1
        for i in range(real_classes):
            if lab[i] == 0:
                continue
            lab[i] = lab[i] / len(cluster)
        score += np.max(lab) * clusters_prob[index]

    return score


def kmeans_clustering(datas, ans, num_classes):
    kmeans = KMeans(n_clusters=num_classes, n_init="auto", max_iter=30000)
    kmeans.fit(datas)

    print("kmeans")
    entropy_score = score_entropy(kmeans.labels_, ans, num_classes, num_classes)
    purity_score = score_purity(kmeans.labels_, ans, num_classes, num_classes)
    print("entropy score: ", entropy_score)
    print("purity score: ", purity_score)
    print()
    return kmeans.labels_


def agglomerative_clustering(datas, ans, num_classes):
    agglomerative = AgglomerativeClustering(c=num_classes, linkage="ward")
    agglomerative.fit(datas)

    print("agglomerative")
    entropy_score = score_entropy(agglomerative.labels_, ans, num_classes, num_classes)
    purity_score = score_purity(agglomerative.labels_, ans, num_classes, num_classes)
    print("entropy score: ", entropy_score)
    print("purity score: ", purity_score)
    print()


def dbscan_clustering(datas, ans, real_classes, eps, min_samples):
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    dbscan.fit(datas)

    label_classes = max(dbscan.labels_) + 1
    noise_num = list(dbscan.labels_).count(-1) / len(dbscan.labels_)
    entropy_score = score_entropy(dbscan.labels_, ans, real_classes, label_classes)
    purity_score = score_purity(dbscan.labels_, ans, real_classes, label_classes)

    if noise_num > 0.2:
        return

    print("dbscan")
    print("noise num: ", noise_num)
    print("entropy score: ", entropy_score)
    print("purity score: ", purity_score)
    print()


def clustering(courses):
    datas, ans = preprocess_data(courses)
    kmean_result = kmeans_clustering(datas, ans, 5)
    agglomerative_clustering(datas, ans, 5)
    dbscan_clustering(datas, ans, 5, 7.0, 3)

    # for i in range(5, 10):
    # for j in range(2, 6):
    #     print("eps: ", i, " min_samples: ", j)
    #     dbscan_clustering(datas, ans, 5, i, j)

    # for i, course in enumerate(courses.values()):
    #     if course.gu_domain[0] not in ["人文藝術", "社會科學", "自然科學", "邏輯運算", "大學入門"]:
    #         continue
    #     print(course.name, kmean_result[i])
