import matplotlib.pyplot as plt
import random
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button


# Bubble Sort Algorithm
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                yield arr


# Selection Sort Algorithm
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
            yield arr
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        yield arr


# Insertion Sort Algorithm
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
            yield arr
        arr[j + 1] = key
        yield arr


# Quick Sort Algorithm
def quick_sort(arr, low, high):
    if low < high:
        pi = yield from partition(arr, low, high)
        yield arr
        yield from quick_sort(arr, low, pi - 1)
        yield from quick_sort(arr, pi + 1, high)


def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            yield arr

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    yield arr
    return i + 1


# Merge Sort Algorithm
def merge_sort(arr, start, end):
    if end - start > 1:
        mid = (start + end) // 2
        yield from merge_sort(arr, start, mid)
        yield from merge_sort(arr, mid, end)
        yield from merge(arr, start, mid, end)


def merge(arr, start, mid, end):
    left = arr[start:mid]
    right = arr[mid:end]
    i = j = 0
    k = start

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1
        yield arr

    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1
        yield arr

    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1
        yield arr


# Heap Sort Algorithm
def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        yield arr
        yield from heapify(arr, n, largest)


def heap_sort(arr):
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        yield arr
        yield from heapify(arr, i, 0)


def comparison_count_sort(arr):
    n = len(arr)
    count = [0] * n

    for i in range(n):
        for j in range(n):
            if arr[j] < arr[i]:
                count[i] += 1
        yield arr

    output = [0] * n
    for i in range(n):
        output[count[i]] = arr[i]
        yield output

    for i in range(n):
        arr[i] = output[i]
        yield arr

# Visualization Function
def visualize(sort_algorithm, arr):
    global anim  # Use a global variable to allow stopping/restarting animations
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.2)  # Reserve space for buttons at the bottom

    bar_rects = ax.bar(range(len(arr)), arr, align="edge")
    ax.set_xlim(0, len(arr))
    ax.set_ylim(0, max(arr) + 1)
    text = ax.text(0.02, 0.95, "", transform=ax.transAxes)
    iteration = [0]

    def update_fig(frame):
        # Update the bar heights
        for rect, val in zip(bar_rects, frame):
            rect.set_height(val)
        iteration[0] += 1
        text.set_text(f"# of operations: {iteration[0]}")

    # Create the animation
    anim = FuncAnimation(
        fig,
        func=update_fig,
        frames=sort_algorithm(arr),
        interval=50,
        repeat=False,
        cache_frame_data=False  # Disable caching to avoid warnings
    )
    plt.show()


# Button Callback for Bubble Sort
def start_bubble_sort(event):
    # global anim  # Stop any ongoing animation
    # if 'anim' in globals():
    #     anim._stop()  # Stop the current animation
    arr = [random.randint(1, 100) for _ in range(50)]
    visualize(bubble_sort, arr.copy())


# Button Callback for Selection Sort
def start_selection_sort(event):
    # global anim  # Stop any ongoing animation
    # if 'anim' in globals():
    #     anim._stop()  # Stop the current animation
    arr = [random.randint(1, 100) for _ in range(50)]
    visualize(selection_sort, arr.copy())


# Button Callback for Insertion Sort
def start_insertion_sort(event):
    # global anim  # Stop any ongoing animation
    # if 'anim' in globals():
    #     anim._stop()  # Stop the current animation
    arr = [random.randint(1, 100) for _ in range(50)]
    visualize(insertion_sort, arr.copy())


# Button Callback for Quick Sort
def start_quick_sort(event):
    # global anim  # Stop any ongoing animation
    # if 'anim' in globals():
    #     anim._stop()  # Stop the current animation
    arr = [random.randint(1, 100) for _ in range(50)]
    visualize(lambda arr: quick_sort(arr, 0, len(arr) - 1), arr.copy())


# Button Callback for Merge Sort
def start_merge_sort(event):
    # global anim  # Stop any ongoing animation
    # if 'anim' in globals():
    #     anim._stop()  # Stop the current animation
    arr = [random.randint(1, 100) for _ in range(50)]
    visualize(lambda arr: merge_sort(arr, 0, len(arr)), arr.copy())


# Button Callback for Heap Sort
def start_heap_sort(event):
    # global anim  # Stop any ongoing animation
    # if 'anim' in globals():
    #     anim._stop()  # Stop the current animation
    arr = [random.randint(1, 100) for _ in range(50)]
    visualize(heap_sort, arr.copy())

# Button Callback for Count Sort
def start_count_sort(event):
    # global anim  # Stop any ongoing animation
    # if 'anim' in globals():
    #     anim._stop()  # Stop the current animation
    arr = [random.randint(1, 100) for _ in range(50)]
    visualize(comparison_count_sort, arr.copy())

# Main Function with Buttons
if __name__ == "__main__":
    # Create the main figure
    # fig, ax = plt.subplots()
    # plt.subplots_adjust(bottom=0.2)  # Reserve space for buttons at the bottom

    # Add buttons
    ax_bubble = plt.axes([0.10, 0.70, 0.2, 0.075])  # [x, y, width, height]
    ax_select = plt.axes([0.40, 0.70, 0.2, 0.075])
    ax_insert = plt.axes([0.70, 0.70, 0.2, 0.075])
    ax_quick = plt.axes([0.10, 0.40, 0.2, 0.075])
    ax_merge = plt.axes([0.40, 0.40, 0.2, 0.075])
    ax_heap = plt.axes([0.70, 0.40, 0.2, 0.075])
    ax_count = plt.axes([0.30, 0.10, 0.4, 0.075])

    btn_bubble = Button(ax_bubble, "Bubble Sort")
    btn_select = Button(ax_select, "Selection Sort")
    btn_insert = Button(ax_insert, "Insertion Sort")
    btn_quick = Button(ax_quick, "Quick Sort")
    btn_merge = Button(ax_merge, "Merge Sort")
    btn_heap = Button(ax_heap, "Heap Sort")
    btn_count = Button(ax_count, "Comparison Counting Sort")

    # Attach callback functions to buttons
    btn_bubble.on_clicked(start_bubble_sort)
    btn_select.on_clicked(start_selection_sort)
    btn_insert.on_clicked(start_insertion_sort)
    btn_quick.on_clicked(start_quick_sort)
    btn_merge.on_clicked(start_merge_sort)
    btn_heap.on_clicked(start_heap_sort)
    btn_count.on_clicked(start_count_sort)

    plt.show()
