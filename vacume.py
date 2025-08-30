def get_turn_radius(shape):
    if shape == 'round':
        return 1
    elif shape == 'square':
        return 2
    elif shape == 'triangle':
        return 3
    elif shape == 'heptagon':
        return 1.5
    else:
        return 2


def simulate_cleaning(shape, room_width, room_height):
    cleaned_cells = 0
    total_steps = 0
    radius = get_turn_radius(shape)

    for y in range(room_height):
        if y % 2 == 0:
            row = range(room_width)
        else:
            row = range(room_width - 1, -1, -1)

        for x in row:
            cleaned_cells += 1
            total_steps += radius

    return cleaned_cells, total_steps


def find_best_shape():
    shapes = ['round', 'square', 'triangle', 'heptagon']
    room_width = 10
    room_height = 10
    shape_results = []

    for shape in shapes:
        cells, time = simulate_cleaning(shape, room_width, room_height)
        shape_results.append((shape, cells, time))

    best_shape = min(shape_results, key=lambda s: s[2])
    return best_shape, shape_results


def show_results(category, item):
    print("\nCleaning Category:", category)
    print("Item:", item)

    best, results = find_best_shape()

    print("\nBest Shape Selected:", best[0].capitalize())
    print("Total Cells Cleaned:", int(best[1]))
    print("Time Taken:", best[2], "steps")

    print("\nTime Taken by Each Shape:")
    for shape, cells, time in results:
        print(f"{shape.capitalize()}: {time} steps")

    print()


def clean_solid():
    print("\nChoose the type of solid:")
    print("1. Dust")
    print("2. Rocks/Papers")
    print("3. Others")
    choice = input("Enter your choice (1-3): ")

    if choice == '1':
        show_results("Solid", "Dust")
    elif choice == '2':
        show_results("Solid", "Rocks/Papers")
    elif choice == '3':
        show_results("Solid", "Others")
    else:
        print("Invalid option. Please try again.")


def clean_liquid():
    print("\nChoose the type of liquid:")
    print("1. Water")
    print("2. Beverage")
    print("3. Others")
    choice = input("Enter your choice (1-3): ")

    if choice == '1':
        show_results("Liquid", "Water")
    elif choice == '2':
        show_results("Liquid", "Beverage")
    elif choice == '3':
        show_results("Liquid", "Others")
    else:
        print("Invalid option. Please try again.")


def start_cleaning():
    print("\nVacuum Started")
    print("1. Solid")
    print("2. Liquid")
    print("3. Back to Main Menu")
    choice = input("Choose the category (1-3): ")

    if choice == '1':
        clean_solid()
    elif choice == '2':
        clean_liquid()
    elif choice == '3':
        return
    else:
        print("Invalid choice. Returning to main menu.")


def turn_left():
    print("Vacuum turned left.")


def turn_right():
    print("Vacuum turned right.")


def dock_vacuum():
    print("Vacuum is docked and not moving.")


def main():
    while True:
        print("\n--- Vacuum Cleaner Menu ---")
        print("1. Start Cleaning")
        print("2. Turn Left")
        print("3. Turn Right")
        print("4. Dock Vacuum")
        print("5. Stop Program")
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            start_cleaning()
        elif choice == '2':
            turn_left()
        elif choice == '3':
            turn_right()
        elif choice == '4':
            dock_vacuum()
        elif choice == '5':
            print("Vacuum program stopped.")
            break
        else:
            print("Invalid input. Please enter a number from 1 to 5.")

main()
