import load_data
import associate
import clustering


def tasks(data):
    associate.associate(data)
    clustering.clustering(data)


if __name__ == "__main__":
    years = ["1121"]
    data = load_data.load_data(years)
    # for d in data["1121"].values():
    #     print(d)

    tasks(data["1121"])
