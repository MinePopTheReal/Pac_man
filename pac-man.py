from src.__main__ import main
from src.message.errors import Error


if __name__ == "__main__":
    try:
        main()
    except Error as e:
        print(e)
    except KeyboardInterrupt:
        print(Error("You have stopped the program"))
