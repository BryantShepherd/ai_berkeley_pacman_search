# Pacman Search

**Điểm cuối cùng**: 


```sh
python2 autograder.py
```

## Câu 1: Perceptron

```py
def train( self, trainingData, trainingLabels, validationData, validationLabels ):
    self.features = trainingData[0].keys()

    ### YOUR CODE HERE ###
    for iteration in range(self.max_iterations):
        print "Starting iteration ", iteration, "..."
        for i in range(len(trainingData)):
            data = trainingData[i]
            # Nhãn của dữ liệu training
            actual = trainingLabels[i]
            # Nhãn được dự đoán
            prediction = self.classify([data])[0]
            if (actual != prediction):
                # update WEIGHT VECTOR of actual label
                self.weights[actual] = self.weights[actual] + data
                self.weights[prediction] = self.weights[prediction] - data

```

## Câu 2: Perceptron Analysis

```py
def findHighWeightFeatures(self, label):
    featuresWeights = []

    ### YOUR CODE HERE ###

    # Sử dụng Priority Queue để có thể lấy top 100 dữ liệu ra nhanh hơn.
    featuresPQ = util.PriorityQueue()

    for i in self.weights[label]:
        featuresPQ.push(i, -self.weights[label][i])

    for i in range(100):
        featuresWeights.append(featuresPQ.pop())

    return featuresWeights
```

## Câu 3: MIRA

```py
def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, Cgrid):

    ### YOUR CODE HERE ###
    for _ in range(self.max_iterations):
        for c in Cgrid:
            for i, data in enumerate(trainingData):
                actual = trainingLabels[i]
                prediction = self.classify([data])[0]

                if (actual != prediction):
                    r = ((self.weights[prediction] - self.weights[actual]) * data + 1 ) * 1.0 / (data * data * 2)
                    r = min(c, r)

                    # compromise for the fact that there is no multiplyAll()
                    # method exist on Counter.
                    f = None
                    if (r == 0):
                        f = data - data
                    else:
                        f = data.copy()
                        f.divideAll(1.0 / r)

                    self.weights[actual] = self.weights[actual] + f
                    self.weights[prediction] = self.weights[prediction] - f
```

## Câu 4: Digit Feature Design

## Câu 5: Behavioral Cloning

```py
def train( self, trainingData, trainingLabels, validationData, validationLabels ):
    self.features = trainingData[0][0]['Stop'].keys() # could be useful later

    ### YOUR CODE HERE ###
    for iteration in range(self.max_iterations):
        print "Starting iteration ", iteration, "..."
        for i in range(len(trainingData)):
            data = trainingData[i]
            prediction = self.classify([data])[0]
            actual = trainingLabels[i]

            print(self.weights)

            if (actual != prediction):
                self.weights = self.weights + data[0][actual] - data[0][prediction]
```

## Câu 6: Pacman Feature Design
