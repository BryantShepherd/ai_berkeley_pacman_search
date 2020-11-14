# Week 5 - Classification

**Điểm cuối cùng**: 21/25 ([demo](https://drive.google.com/drive/folders/1BRJi0Ny_5gtQWpAHH3RmvLJTeJLfhrv7?usp=sharing))

![final](https://imgur.com/download/Bjzq6tZ/)

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

    # Tìm các weight vector sau khi được huấn luyện bởi c
    potentialWeights = {}
    for c in Cgrid:
        # Tạo weight vector tạm thời
        tempWeight = self.weights.copy()
        for _ in range(self.max_iterations):
            for i, data in enumerate(trainingData):
                actual = trainingLabels[i]
                prediction = self.classifyWeight([data], tempWeight)[0]

                if (actual != prediction):
                    r = ((tempWeight[prediction] - tempWeight[actual]) * data + 1.0 ) / (data * data * 2)
                    r = min(c, r)

                    # compromise for the fact that there is no multiplyAll()
                    # method exist on Counter.
                    f = None
                    if (r == 0):
                        f = data - data
                    else:
                        f = data.copy()
                        f.divideAll(1.0 / r)

                    tempWeight[actual] = tempWeight[actual] + f
                    tempWeight[prediction] = tempWeight[prediction] - f
        potentialWeights[c] = tempWeight

    # Đánh giá c bằng cách kiểm tra với validationData
    maxScore = float("-inf")
    maxAccuracyC = float("inf")

    for c in Cgrid:
        score = 0
        for i, data in enumerate(validationData):
            actual = validationLabels[i]
            prediction = self.classifyWeight([data], potentialWeights[c])[0]
            if (actual == prediction): score += 1

        if (score >= maxScore):
            # Nếu hai kết quả bằng nhau, lấy giá trị c nhỏ nhất
            maxAccuracyC = min(c, maxAccuracyC) if score == maxScore else c
            maxScore = score

    self.weights = potentialWeights[maxAccuracyC]
    self.weights["c"] = maxAccuracyC

def classifyWeight(self, data, weights):
    """
    Chức năng tương tự như self.classify, chỉ khác là sử dụng
    weight vector riêng.
    """
    guesses = []
    for datum in data:
        vectors = util.Counter()
        for l in self.legalLabels:
            vectors[l] = weights[l] * datum
        guesses.append(vectors.argMax())
    return guesses
```

## Câu 4: Digit Feature Design

**Đọc hiểu** ([nguồn](https://github.com/DarthWindu007/classification-ai/blob/master/dataClassifier.py))

```py
def flooding(datum, x, y, marked):
    """
    Hàm sử dụng thuât toán flooding để đánh dấu các vùng
    pixel trắng.

    Cụ thể hơn, hàm bắt đầu với một điểm có tọa độ (x, y) và thực
    hiện đánh dấu (x, y) và 4 điểm pixel trắng xung quanh. Hàm sẽ tiếp tục gọi
    đệ quy cho đến khi đánh dấu toàn bộ pixel trắng ở cạnh nhau.
    """

    # Mảng đánh dấu (xem đã duyệt qua điểm (x, y) hay chưa)
    marked[x][y] = 1

    # Mảng 4 pixel gần với (x, y)
    adjacentPixels = []

    if (x != 0): adjacentPixels.append((x - 1, y))
    if (x != DIGIT_DATUM_WIDTH - 1): adjacentPixels.append((x + 1, y))
    if (y != 0): adjacentPixels.append((x, y - 1))
    if (y != DIGIT_DATUM_HEIGHT - 1): adjacentPixels.append((x, y + 1))

    for px, py in adjacentPixels:
        # Nếu (px, py) là pixel trắng và chưa đựợc duyệt, gọi đệ quy.
        if (datum.getPixel(px, py) == 0 and marked[px][py] == 0):
            marked = flooding(datum, px, py, marked)

    return marked

def enhancedFeatureExtractorDigit(datum):
    """
    Sử dụng thuật toán flooding để tìm số vùng
    pixel trắng, sau đó thêm vào feature.
    """
    features = basicFeatureExtractorDigit(datum)

    # Khởi tạo hàm đánh dấu
    marked = [[0 for j in range(DIGIT_DATUM_HEIGHT)] for i in range(DIGIT_DATUM_WIDTH)]
    # Số vùng pixel trắng.
    number_of_regions = 0

    for x in range(DIGIT_DATUM_WIDTH):
        for y in range(DIGIT_DATUM_HEIGHT):
            if (marked[x][y] == 0 and datum.getPixel(x, y) == 0):
                marked = flooding(datum, x, y, marked)
                # Sau khi đánh dấu xong một vùng pixel trắng,
                # tăng biến đếm lên 1.
                number_of_regions += 1

    # Do các số có tối đa số vùng trắng là 3,
    # đặt features[số vùng] là 1, còn lại là 0.
    features[1] = 0
    features[2] = 0
    features[3] = 0
    features[number_of_regions] = 1
    return features
```

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

            if (actual != prediction):
                self.weights = self.weights + data[0][actual] - data[0][prediction]
```

## Câu 6: Pacman Feature Design
