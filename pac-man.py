from src.message.errors import Error
from src.__main__ import main


if __name__ == "__main__":
    try:
        main()
    except Error as e:
        print(e)
    except KeyboardInterrupt:
        print(Error("You have stopped the program"))