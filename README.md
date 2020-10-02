# Pacman Search

**Điểm cuối cùng**: 24/25

![autograder](https://i.imgur.com/l91Cj7V.gif)

**Lưu ý**: Project Pacman Search ban đầu được viết bằng Python 2, tuy nhiên project đã được chuyển về Python 3 để có thể sử dụng cú pháp và chức năng mới nhất do Python cung cấp.

```sh
python3 pacman.py
```

## Câu hỏi 1-4

Bốn câu hỏi đầu tiên có cấu trúc tương tự nhau, chỉ khác về cấu trúc dữ liệu sử dụng để lưu trữ state.

Chương trình bắt đầu bằng việc khởi tạo các biến cần thiết `visited`, `stateStack`. Phần tử của `stateStack` là các tuple có dạng `(state, actions, cost)` - lưu trữ vị trí, các bước để di chuyển từ vị trí ban đầu tới đó và tổng chi phí di chuyển.

Đầu tiên, chương trình sẽ push trạng thái ban đầu của pacman vào `stateStack`. Sau đó, chương trình sẽ thực hiện vòng lặp:

1. Pop trạng thái từ `stateStack`
2. Nếu trạng thái đó là trạng thái đích, trả về các bước di chuyển và kết thúc chương trình. Nếu không, đi đến bước 3.
3. Nếu trạng thái đã được xét, bỏ qua vòng lặp. Nếu không, đi đến bước 4.
4. Thêm trạng thái vào tập các state đã đi qua.
5. Lấy ra danh sách successor của trạng thái đang xét, update danh sách bước di chuyển và chi phí của successor đó, và thêm nó vào `stateStack`.
6. Lặp lại cho tới khi không còn phần tử nào nằm trong `stateStack`.

```python
# depthFirstSearch()
# Lưu các vị trí đã đi qua
visited = set()

# Lưu danh sách các state, có dạng (state, action, cost)
stateStack = util.Stack()

# Push trạng thái ban đầu vào stack
stateStack.push((problem.getStartState(), [], 0))

while not stateStack.isEmpty():
    cState, cActions, cCost = stateStack.pop()

    if (problem.isGoalState(cState)):
        return cActions

    if (cState in visited):
        continue

    visited.add(cState)

    # Lặp qua danh sách các successor của state hiện tại và push successor vào stateStack.
    for successor in problem.getSuccessors(cState):
        sState, nextAction, nextCost = successor

        # Cập nhật các bước di chuyển và chi phí để tới được state này.
        sActions = cActions + [nextAction]
        sCost = cCost + nextCost

        stateStack.push((sState, sActions, sCost))

return []
```

Thuật toán BFS, UCS và A\* có cấu trúc tương tự như trên. Thay vì cấu trúc dữ liệu Stack, BFS sử dụng Queue, UCS và A\* sử dụng PriorityQueue với priority lần lượt là `cost` và `manhattanDistance + cost`.

## Câu hỏi 5

- State: vị trí của pacman, trạng thái của 4 góc bản đồ.

- Action: NSEW

- Successor: Update vị trí của pacman và trạng thái của 4 góc bản đồ (nếu cần)

- Goal test: Trạng thái của 4 góc bản đồ là True (đã đi qua hết).

## Câu hỏi 6: Corners Problem: Heuristic

Ta ước lượng chi phí để đạt được trạng thái đích là đi đến được góc xa nhất của bản đồ. Sử dụng hàm này, agent sẽ có xu hướng expand các node ra 4 góc bản đồ, giúp tìm kiếm đường đi tối ưu nhanh hơn.

Hàm có tính admissible do để đi qua được 4 góc thì agent buộc phải đi qua góc ở xa nhất. Hàm cũng đảm bảo tính consistency do biểu thức h(n) \<= g(n, n') + h(n') luôn thỏa mãn.

```py
corners = problem.corners
walls = problem.walls

currentPosition, currentCornersBoolean = state

maxDist = float('-inf')

if currentCornersBoolean == (True, True, True, True):
    return 0

for i in range(len(currentCornersBoolean)):
    dist = util.manhattanDistance(currentPosition, corners[i])
    if (not currentCornersBoolean[i] and dist > maxDist):
        maxDist = dist

return maxDist
```

## Câu hỏi 7: Eating All The Dots

Tương tự như câu hỏi 6, để ăn tất cả hạt trên bản đồ, agent cần phải ăn được hạt ở xa nhất.

```py
position, foodGrid = state
maxDist = float('-inf')
count = foodGrid.count()
if count == 0:
    return 0

for i in range(foodGrid.width):
    for j in range(foodGrid.height):
        if (foodGrid.data[i][j] and util.manhattanDistance(position, (i, j)) > maxDist):
            maxDist = util.manhattanDistance(position, (i, j))
return maxDist
```

## Câu hỏi 8: Suboptimal Search

Sử dụng hàm `search.uniformCostSearch()` của câu 3 để tìm.
