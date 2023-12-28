class Course:
    def __init__(self, meta_data, info_data, people_data) -> None:
        self.serial = meta_data["serial"]  # 開課序號
        self.year = int(meta_data["year"])  # 學年度
        self.term = int(meta_data["term"])  # 學期
        self.name = meta_data["name"]  # 課程名稱
        self.teachers = info_data["teacher"].split()  # 授課教師
        self.credit = int(meta_data["credit"])  # 學分數
        self.gu_domain = (
            people_data["中文課程名稱"].item().split("109起入學：")[1].split()[:-1]
        )  # 通識領域
        self.description = info_data["description"]  # 課程說明
        self.method = info_data["methods"]  # 教學方法
        self.evaluations = info_data["evaluations"]  # 評量方式
        self.quota_limit = meta_data["quota"]["limit"]  # 限修人數
        self.quota_additional = meta_data["quota"]["additional"]  # 加簽人數
        self.people = people_data["選修人數"].item()  # 選修人數
        self.day = meta_data["schedule"][0]["day"]  # 上課星期
        self.time_from = meta_data["schedule"][0]["from"]  # 上課開始時間
        self.time_to = meta_data["schedule"][0]["to"]  # 上課結束時間
        self.campus = meta_data["schedule"][0]["campus"]  # 上課地點
        self.classroom = meta_data["schedule"][0]["classroom"]  # 上課教室
        self.program = meta_data["programs"]  # 學程
        self.emi = True if people_data["全英語"].item() == "是" else False  # 全英語

    def __str__(self) -> str:
        return f"開課序號: {self.serial} 學年度: {self.year} 學期: {self.term} 課程名稱: {self.name} 通識領域: {self.gu_domain} 授課教師: {self.teachers} 學分數: {self.credit} 選修人數: {self.people} 全英語: {self.emi}"
