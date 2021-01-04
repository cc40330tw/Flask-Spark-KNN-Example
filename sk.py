

def turn_iris_to_sc():
    from sklearn import datasets
    iris = datasets.load_iris()
    iris_target = iris['target']
    table = [list(e) for e in zip(iris['data'].tolist(), iris['target'])]
    return table


print(turn_iris_to_sc())