# AI Assignment Repository

Kho lưu trữ bài tập minh họa về Trí tuệ Nhân tạo trong môn học, bao gồm:
- Robot hút bụi sử dụng các thuật toán tìm kiếm
- Bài toán tô màu bản đồ thỏa ràng buộc Constraint Satisfaction Problems (CSP)
- Trò chơi Tic Tac Toe với AI

## 1. Vacuum Cleaner Robot

Bài tập mô phỏng một robot hút bụi di chuyển trên một lưới để làm sạch các ô bẩn bằng các thuật toán tìm kiếm khác nhau.

### Các thuật toán sử dụng
- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- Iterative Deepening Search (IDS)
- Uniform Cost Search (UCS)
- Greedy Search
- A* Search
- Iterative Deepening A* (IDA*)
- Simple Hill Climbing
- Steepest Ascent Hill Climbing
- Stochastic Hill Climbing
- Random Restart Hill Climbing
- Local Beam Search
- Simulated Annealing
- Partial Observation Search

### Các file
- ROOMBA\main.py: file chính khởi động chương trình
- ROOMBA\partial_observation.py: triển khai thuật toán tìm kiếm có quan sát một phần
- ROOMBA\roomba_algos.py: triển khai các thuật toán còn lại
- ROOMBA\roomba_node.py: class node và hàm tạo map ngẫu nhiên
- ROOMBA\roomba_gui.py: giao diện đồ họa

### Cách chạy
```
python3 ROOMBA\main.py
```

## 2. CSP Map Coloring

Bài tập áp dụng CSP để tô 4 màu trên bản đồ Việt Nam 63 tỉnh thành sao cho các vùng lân cận không có cùng màu.

### Các thuật toán sử dụng
- Backtracking
- Forward Checking
- Backtracking + AC-3
- Min-Conflicts

### Các file
- CSP MAP COLORING\main.py: file chính khởi động chương trình, tô màu và lưu 4 ảnh PNG cho 4 thuật toán
- CSP MAP COLORING\solvers.py: triển khai các thuật toán CSP
- CSP MAP COLORING\visualizer.py: hàm trợ giúp lưu ảnh và hiển thị ảnh
- CSP MAP COLORING\geodata.py: đọc dữ liệu geojson
- CSP MAP COLORING\borders.geojson: dữ liệu bản đồ
- CSP MAP COLORING\show_map.ipynb: file python notebook cho phép xem kết quả bản đồ trực tiếp khi chạy trong VSCode

### Cách chạy
```
pip install geopandas
python3 "CSP MAP COLORING\main.py"
```

Kết quả sẽ được lưu dưới dạng các file hình ảnh PNG trong thư mục CSP MAP COLORING.

## 3. Tic Tac Toe

Bài tập xây dựng trò chơi Tic Tac Toe với AI chơi đối kháng bằng các thuật toán quyết định.

### Các thuật toán sử dụng
- Minimax
- Alpha-Beta
- Expectimax

### Các file
- TIC TAC TOE/tic_tac_toe.py: toàn bộ game và thuật toán AI

### Cách chạy
```
python3 "TIC TAC TOE\tic_tac_toe.py"
```

## Môi trường chạy
- Python 3.9 trở lên
- Có thể cần cài đặt các thư viện sau:

```
pip install pygame geopandas
```
