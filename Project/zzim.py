class ZZIM:
    def __init__(self):
        self.zzimlist = list()
    def get_zzimlist(self):
        return self.zzimlist
    def add_zzim(self,data): # 해당 컨텐츠의 전체 데이터를 가져옴
        self.zzimlist.append(data)
