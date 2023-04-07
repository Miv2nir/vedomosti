class Aggregator:
    def __init__(self):
        pass

    def aggregate(self, data):
        raise Exception("Not implemented!")


class SumAggregator(Aggregator):
    def __init__(self):
        Aggregator.__init__(self)

    def aggregate(self, data):
        # assuming last column is score
        # print("AGG data:", data)
        return data[-1]


class LastThreeAggregator(Aggregator):
    def __init__(self):
        Aggregator.__init__(self)

    def aggregate(self, data):
        # assuming last column is score
        # print("AGG data:", data)
        return sum(data[-4:-1])


class UniformWeightedAggregator(Aggregator):
    def __init__(self):
        Aggregator.__init__(self)

    def aggregate(self, data):
        # assuming last column is score
        # print("AGG data:", data)
        return sum(data[:-1]) * 10 / len(data[:-1])

class ManualCheckAggregator(Aggregator):
    def __init__(self):
        Aggregator.__init__(self)

    def aggregate(self, data):
        # assuming last column is score
        return data[-1]
