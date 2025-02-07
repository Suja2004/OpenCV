import pygame
import heapq

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)  # Open set
DARK_GRAY = (105, 105, 105)   # Closed set

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 800
BUTTON_HEIGHT = 100  # Reserve 100 pixels for buttons
GRID_HEIGHT = HEIGHT - BUTTON_HEIGHT

# Grid dimensions
ROWS, COLS = 50, 50
CELL_SIZE = GRID_HEIGHT // ROWS  # Adjust cell size based on grid height

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding Visualizer")

# Node class for each cell in the grid
class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.color = WHITE
        self.neighbors = []

    def get_pos(self):
        return self.row, self.col

    def is_barrier(self):
        return self.color == BLACK

    def reset(self):
        self.color = WHITE

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = GREEN

    def make_end(self):
        self.color = RED

    def make_path(self):
        self.color = BLUE

    def make_open(self):
        self.color = LIGHT_BLUE

    def make_closed(self):
        self.color = DARK_GRAY

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.row * CELL_SIZE, self.col * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def heuristic(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def reconstruct_bidirectional_path(came_from_start, came_from_end, intersection, draw):
    # Reconstruct path from start to intersection
    current = intersection
    while current in came_from_start:
        current = came_from_start[current]
        current.make_path()
        draw()

    # Reconstruct path from end to intersection
    current = intersection
    while current in came_from_end:
        current = came_from_end[current]
        current.make_path()
        draw()

def a_star(draw, grid, start, end):
    count = 0
    open_set = []
    heapq.heappush(open_set, (0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = heapq.heappop(open_set)[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    heapq.heappush(open_set, (f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()  # Mark as part of the open set

        draw()

        if current != start:
            current.make_closed()  # Mark as explored

    return False

def dijkstra(draw, grid, start, end):
    count = 0
    open_set = []
    heapq.heappush(open_set, (0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    open_set_hash = {start}

    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = heapq.heappop(open_set)[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                if neighbor not in open_set_hash:
                    count += 1
                    heapq.heappush(open_set, (g_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()  # Mark as part of the open set

        draw()

        if current != start:
            current.make_closed()  # Mark as explored

    return False

def bfs(draw, grid, start, end):
    queue = [start]
    visited = set()
    came_from = {}

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = queue.pop(0)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited and not neighbor.is_barrier():
                queue.append(neighbor)
                visited.add(neighbor)
                came_from[neighbor] = current
                neighbor.make_open()  # Mark as part of the open set

        draw()

        if current != start:
            current.make_closed()  # Mark as explored

    return False

def dfs(draw, grid, start, end):
    stack = [start]
    visited = set()
    came_from = {}

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = stack.pop()

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        if current not in visited:
            visited.add(current)

            for neighbor in current.neighbors:
                if neighbor not in visited and not neighbor.is_barrier():
                    stack.append(neighbor)
                    came_from[neighbor] = current
                    neighbor.make_open()  # Mark as part of the open set

        draw()

        if current != start:
            current.make_closed()  # Mark as explored

    return False

def greedy_best_first_search(draw, grid, start, end):
    count = 0
    open_set = []
    heapq.heappush(open_set, (0, count, start))
    came_from = {}
    open_set_hash = {start}

    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = heapq.heappop(open_set)[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if neighbor not in open_set_hash and not neighbor.is_barrier():
                came_from[neighbor] = current
                count += 1
                heapq.heappush(open_set, (heuristic(neighbor.get_pos(), end.get_pos()), count, neighbor))
                open_set_hash.add(neighbor)
                neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

def bidirectional_search(draw, grid, start, end):
    queue_start = [start]
    queue_end = [end]
    visited_start = {start}
    visited_end = {end}
    came_from_start = {}
    came_from_end = {}

    def intersect(visited_a, visited_b):
        return any(node in visited_b for node in visited_a)

    while queue_start and queue_end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Expand from start
        current_start = queue_start.pop(0)
        for neighbor in current_start.neighbors:
            if neighbor not in visited_start and not neighbor.is_barrier():
                queue_start.append(neighbor)
                visited_start.add(neighbor)
                came_from_start[neighbor] = current_start
                neighbor.make_open()
                if neighbor in visited_end:  # Intersection found
                    reconstruct_bidirectional_path(came_from_start, came_from_end, neighbor, draw)
                    return True

        draw()

        if current_start != start:
            current_start.make_closed()

        # Expand from end
        current_end = queue_end.pop(0)
        for neighbor in current_end.neighbors:
            if neighbor not in visited_end and not neighbor.is_barrier():
                queue_end.append(neighbor)
                visited_end.add(neighbor)
                came_from_end[neighbor] = current_end
                neighbor.make_open()
                if neighbor in visited_start:  # Intersection found
                    reconstruct_bidirectional_path(came_from_start, came_from_end, neighbor, draw)
                    return True

        draw()

        if current_end != end:
            current_end.make_closed()

    return False

def iddfs(draw, grid, start, end):
    def dls(current, depth, visited, came_from):
        if current == end:
            return True
        if depth == 0:
            return False

        for neighbor in current.neighbors:
            if neighbor not in visited and not neighbor.is_barrier():
                visited.add(neighbor)
                came_from[neighbor] = current
                neighbor.make_open()
                if dls(neighbor, depth - 1, visited, came_from):
                    return True
                neighbor.make_closed()

        return False

    max_depth = ROWS * COLS  # Maximum possible depth
    for depth in range(max_depth):
        visited = set()
        came_from = {}
        if dls(start, depth, visited, came_from):
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        draw()

    return False

def make_grid(rows, cols):
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(cols):
            node = Node(i, j)
            grid[i].append(node)
    return grid

def draw_grid(screen, rows, cols):
    for i in range(rows):
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))
        for j in range(cols):
            pygame.draw.line(screen, BLACK, (j * CELL_SIZE, 0), (j * CELL_SIZE, GRID_HEIGHT))

def draw(screen, grid, rows, cols):
    screen.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(screen)
    draw_grid(screen, rows, cols)

    # Draw buttons
    draw_button(screen, "A*", 10, GRID_HEIGHT + 10, 80, 40, GRAY if algorithm == "A*" else WHITE)
    draw_button(screen, "Dijkstra", 100, GRID_HEIGHT + 10, 120, 40, GRAY if algorithm == "Dijkstra" else WHITE)
    draw_button(screen, "BFS", 230, GRID_HEIGHT + 10, 80, 40, GRAY if algorithm == "BFS" else WHITE)
    draw_button(screen, "DFS", 320, GRID_HEIGHT + 10, 80, 40, GRAY if algorithm == "DFS" else WHITE)
    draw_button(screen, "Greedy", 410, GRID_HEIGHT + 10, 120, 40, GRAY if algorithm == "Greedy" else WHITE)
    draw_button(screen, "Bi-Search", 540, GRID_HEIGHT + 10, 120, 40, GRAY if algorithm == "Bi-Search" else WHITE)
    draw_button(screen, "IDDFS", 670, GRID_HEIGHT + 10, 80, 40, GRAY if algorithm == "IDDFS" else WHITE)

    pygame.display.update()

def draw_button(screen, text, x, y, width, height, color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    font = pygame.font.SysFont(None, 36)
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, (x + 10, y + 5))

def update_neighbors(grid):
    for row in grid:
        for node in row:
            node.neighbors = []
            if node.row > 0 and not grid[node.row - 1][node.col].is_barrier():  # UP
                node.neighbors.append(grid[node.row - 1][node.col])
            if node.row < len(grid) - 1 and not grid[node.row + 1][node.col].is_barrier():  # DOWN
                node.neighbors.append(grid[node.row + 1][node.col])
            if node.col > 0 and not grid[node.row][node.col - 1].is_barrier():  # LEFT
                node.neighbors.append(grid[node.row][node.col - 1])
            if node.col < len(grid[0]) - 1 and not grid[node.row][node.col + 1].is_barrier():  # RIGHT
                node.neighbors.append(grid[node.row][node.col + 1])

def main():
    global algorithm
    grid = make_grid(ROWS, COLS)
    start = None
    end = None
    run = True
    algorithm = "A*"  # Default algorithm

    while run:
        draw(screen, grid, ROWS, COLS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # Left mouse button
                pos = pygame.mouse.get_pos()
                x, y = pos

                # Check if a button was clicked
                if 10 <= x <= 90 and GRID_HEIGHT + 10 <= y <= GRID_HEIGHT + 50:
                    algorithm = "A*"
                elif 100 <= x <= 220 and GRID_HEIGHT + 10 <= y <= GRID_HEIGHT + 50:
                    algorithm = "Dijkstra"
                elif 230 <= x <= 310 and GRID_HEIGHT + 10 <= y <= GRID_HEIGHT + 50:
                    algorithm = "BFS"
                elif 320 <= x <= 400 and GRID_HEIGHT + 10 <= y <= GRID_HEIGHT + 50:
                    algorithm = "DFS"
                elif 410 <= x <= 530 and GRID_HEIGHT + 10 <= y <= GRID_HEIGHT + 50:
                    algorithm = "Greedy"
                elif 540 <= x <= 660 and GRID_HEIGHT + 10 <= y <= GRID_HEIGHT + 50:
                    algorithm = "Bi-Search"
                elif 670 <= x <= 750 and GRID_HEIGHT + 10 <= y <= GRID_HEIGHT + 50:
                    algorithm = "IDDFS"

                # Handle grid interactions
                elif y < GRID_HEIGHT:
                    row, col = x // CELL_SIZE, y // CELL_SIZE
                    if row < ROWS and col < COLS:
                        node = grid[row][col]
                        if not start and node != end:
                            start = node
                            start.make_start()
                        elif not end and node != start:
                            end = node
                            end.make_end()
                        elif node != end and node != start:
                            node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # Right mouse button
                pos = pygame.mouse.get_pos()
                x, y = pos
                if y < GRID_HEIGHT:
                    row, col = x // CELL_SIZE, y // CELL_SIZE
                    node = grid[row][col]
                    node.reset()
                    if node == start:
                        start = None
                    elif node == end:
                        end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    update_neighbors(grid)
                    if algorithm == "A*":
                        a_star(lambda: draw(screen, grid, ROWS, COLS), grid, start, end)
                    elif algorithm == "Dijkstra":
                        dijkstra(lambda: draw(screen, grid, ROWS, COLS), grid, start, end)
                    elif algorithm == "BFS":
                        bfs(lambda: draw(screen, grid, ROWS, COLS), grid, start, end)
                    elif algorithm == "DFS":
                        dfs(lambda: draw(screen, grid, ROWS, COLS), grid, start, end)
                    elif algorithm == "Greedy":
                        greedy_best_first_search(lambda: draw(screen, grid, ROWS, COLS), grid, start, end)
                    elif algorithm == "Bi-Search":
                        bidirectional_search(lambda: draw(screen, grid, ROWS, COLS), grid, start, end)
                    elif algorithm == "IDDFS":
                        iddfs(lambda: draw(screen, grid, ROWS, COLS), grid, start, end)

    pygame.quit()

main()