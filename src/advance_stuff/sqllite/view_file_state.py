from persist_file_state import print_all_statuses, get_file_status


def main():
    while True:
        print("\nFile Status Viewer")
        print("1. View all file statuses")
        print("2. Check specific file status")
        print("3. Quit")

        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            print_all_statuses()
        elif choice == '2':
            filename = input("Enter filename to check: ")
            status, timestamp = get_file_status(filename)
            print(f"Status of {filename}: {status} (Last updated: {timestamp})")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

    print("File Status Viewer stopped.")


if __name__ == "__main__":
    main()