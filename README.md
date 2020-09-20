# Pacman Search

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

Thuật toán BFS, UCS và A\* có cấu trúc tương tự như trên. Thay vì cấu trúc dữ liệu Stack, BFS sử dụng Queue, UCS và A* sử dụng PriorityQueue với priority lần lượt là `cost` và `manhattanDistance + cost`.

