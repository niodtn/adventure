import sys


def main():
    print("Hello from shot!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("python main.py <sound file path>")
        sys.exit(1)

    path = sys.argv[1]
    print(f"{path}")

    main()
