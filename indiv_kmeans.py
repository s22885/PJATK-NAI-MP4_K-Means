import math
import random


class Kmeans:
    vecs: list = []
    means: list = []
    dim: int
    k: int
    stop_prop: float
    e: float

    def __init__(self, dim, k, stop_prop):
        self.dim = dim
        self.k = k
        self.stop_prop = stop_prop

    def aggregate_vecs(self):
        for vi in range(len(self.vecs)):
            aggr_val = []
            for mi in range(len(self.means)):
                tmp_mean = self.means[mi]
                tmp_vec = self.vecs[vi][0]
                res = 0
                for pos in range(len(tmp_mean)):
                    res += math.pow(tmp_vec[pos] - tmp_mean[pos], 2)
                aggr_val.append(res)
            tmp_min = 0
            for i in range(1, len(aggr_val)):
                if aggr_val[tmp_min] > aggr_val[i]:
                    tmp_min = i
            self.vecs[vi][1] = tmp_min

    def aggregate_means(self):
        tmp_means = self.means.copy()
        tmp_in_mean = []
        for im in range(len(tmp_means)):
            tmp_in_mean.append(0)
            for iv in range(len(tmp_means[im])):
                tmp_means[im][iv] = 0
        for vec in self.vecs:
            tmp_in_mean[vec[1]] += 1
            i = 0
            for vec_val in vec[0]:
                tmp_means[vec[1]][i] += vec_val
                i += 1
        for im in range(len(tmp_means)):
            for imv in range(len(tmp_means[im])):
                if tmp_in_mean[imv != 0]:
                    tmp_means[im][imv] /= tmp_in_mean[im]
        self.means = tmp_means

    def to_text(self):
        self.vecs.sort(key=Kmeans.sort_fun)
        res = "group;"
        for i in range(self.dim - 1):
            res += f"dim_{i};"
        res += f"dim_{self.dim}\n"
        for vec_i in self.vecs:
            for vec_pos in range(len(vec_i[0]) - 1):
                res+=f"{vec_i[0][vec_pos]};"
            res += f"{vec_i[0][len(vec_i[0])-1]}\n"
        return res

    def calc_e(self):
        res = 0
        for vec in self.vecs:
            dist = 0
            i = 0
            for vec_val in vec[0]:
                tmp = self.means[vec[1]][i]
                dist += math.pow(tmp - vec_val, 2)
                i += 1
            res += dist
        return res

    def compute(self):
        if len(self.vecs) == 0:
            return False
        if len(self.means) == 0:
            self.init_means()
            self.e = -1

        self.aggregate_vecs()
        self.aggregate_means()
        tmp_e = self.calc_e()
        while math.fabs(tmp_e - self.e) > self.stop_prop:
            self.e = tmp_e
            self.aggregate_vecs()
            self.aggregate_means()
            tmp_e = self.calc_e()
        self.e = tmp_e
        return True

    def init_means(self):
        random.shuffle(self.vecs)
        for i in range(self.k):
            tmp_val = self.vecs[i % self.k][0]
            res = []
            for v in tmp_val:
                res.append(v)
            self.means.append(res)

    def add_vec(self, vec: list):
        if len(vec) == self.dim:
            self.vecs.append([vec, -1])
            return True
        return False

    def add_vecs(self, vecs: list):
        res = [0, 0]
        for vec in vecs:
            tmp = self.add_vec(vec)
            if tmp:
                res[0] += 1
            else:
                res[1] += 1
        return res

    @staticmethod
    def new_kmeans(dim, k, stop_prop):
        if dim < 1 or k < 1 or stop_prop < 0:
            return None
        return Kmeans(dim, k, stop_prop)

    @staticmethod
    def sort_fun(e):
        return e[1]
