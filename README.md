# Pacman Search

**Điểm cuối cùng**: 24/25

**Lưu ý**: Project Pacman Search ban đầu được viết bằng Python 2, tuy nhiên project đã được chuyển về Python 3 để có thể sử dụng cú pháp và chức năng mới nhất do Python cung cấp.

```sh
python3 pacman.py
python3 autograder.py
```

## Câu hỏi 1: Reflex Agent

```python
# Khoảng cách tới bé ma gần nhất
minDistanceToGhost = min(util.manhattanDistance(
    newPos, ghost.getPosition()) for ghost in newGhostStates)

# Khoảng cách tới miếng thức ăn gần nhất. Giá trị này được nghịch đảo trong
# giá trị trả về để khuyến khích pacman đi tới miếng thức ăn gần nhất.
closestFood = float('inf')
for foodPos in newFood.asList():
    if (util.manhattanDistance(newPos, foodPos) < closestFood):
        closestFood = util.manhattanDistance(newPos, foodPos)

# Giới hạn khoảng cách tới bé ma gần nhất để tránh pacman chạy xa quá mà quên mất ăn
if (minDistanceToGhost >= 4):
    minDistanceToGhost = 4

# Tổng của khoảng cách ngắn nhất tới ma, điểm hiện tại và nghịch đảo khoảng cách tới
# miếng thức ăn gần nhất
return minDistanceToGhost + successorGameState.getScore() + 1.0 / closestFood
```

## Câu hỏi 2: Minimax

```python
def getValue(self, gameState, turn):
    """
    Trả về giá trị của trạng thái này. Chương trình có lưu một biến
    turn để quản lý lượt đi và để xác định độ sâu hiện tại để dừng đệ quy.
    """
    agentIndex = turn % gameState.getNumAgents()
    if turn >= self.depth * gameState.getNumAgents() or gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState), None

    if agentIndex == 0:
        value, action = self.getMaxValue(gameState, agentIndex, turn)
    else:
        value, action = self.getMinValue(gameState, agentIndex, turn)

    return value, action

def getMaxValue(self, gameState, agentIndex, turn):
    maxValue, maxAction = float('-inf'), None
    for action in gameState.getLegalActions(agentIndex):
        successor = gameState.generateSuccessor(agentIndex, action)
        value, _ = self.getValue(successor, turn + 1)
        if (value > maxValue):
            maxValue = value
            maxAction = action
    return maxValue, maxAction

def getMinValue(self, gameState, agentIndex, turn):
    minValue, minAction = float('inf'), None
    for action in gameState.getLegalActions(agentIndex):
        successor = gameState.generateSuccessor(agentIndex, action)
        value, _ = self.getValue(successor, turn + 1)
        if (value < minValue):
            minValue = value
            minAction = action
    return minValue, minAction

def getAction(self, gameState):
  _, maxAction = self.getValue(gameState, 0)
  return maxAction
```

## Câu hỏi 3: Alpha-Beta Pruning

Thuật toán Alpha-Beta Pruning được cài đặt tương tự như thuật toán Minimax trongtrong câu 2. Điểm khác biệt là trong quá trình đánh giá một state, chương trình sẽ so sánh giá trị đó với alpha và beta để dừng quá trình duyệt cây và return luôn.

```python
def getMaxValue(self, gameState, agentIndex, turn, alpha, beta):
    maxValue, maxAction = float('-inf'), None
    for action in gameState.getLegalActions(agentIndex):
        successor = gameState.generateSuccessor(agentIndex, action)
        value, _ = self.getValue(successor, turn + 1, alpha, beta)
        if (value > maxValue):
            maxValue = value
            maxAction = action
        if value > beta:
            return value, action
        alpha = max(value, alpha)
    return maxValue, maxAction

def getMinValue(self, gameState, agentIndex, turn, alpha, beta):
    minValue, minAction = float('inf'), None
    for action in gameState.getLegalActions(agentIndex):
        successor = gameState.generateSuccessor(agentIndex, action)
        value, _ = self.getValue(successor, turn + 1, alpha, beta)
        if (value < minValue):
            minValue = value
            minAction = action
        if value < alpha:
            return value, action
        beta = min(value, beta)
    return minValue, minAction
```

## Câu hỏi 4: Expectimax

Thuật toán Expectimax cũng được cài đặt tương tự như Minimax trong câu 2. Thay vì giả định đối thủ sử dụng thuật toán tối ưu, thuật toán cho rằng đối thủ có thể đưa ra các nước đi ngẫu nhiên. Vì vậy, giá trị minValue của nước đi đối thủ được tính là trung bình của tổng giá trị các successor.

```py
def getWeightedMinValue(self, gameState, agentIndex, turn):
    values = []
    actions = gameState.getLegalActions(agentIndex)
    for action in actions:
        successor = gameState.generateSuccessor(agentIndex, action)
        value, _ = self.getValue(successor, turn + 1)
        values.append(value)

    randomIndex = random.randrange(0, len(actions))

    # Tính trung bình tổng giá trị của successor
    avgValue = sum(values) * 1.0 / len(actions)

    return avgValue, actions[randomIndex]
```

## Câu hỏi 5: Evaluation Function
