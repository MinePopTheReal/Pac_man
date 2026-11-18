from src.message.errors import Error


if __name__ == "__main__":
    try:
        from src.__main__ import main
        main()
    except Error as e:
        print(e)
    except KeyboardInterrupt:
        print(Error("You have stopped the program"))
    except Exception as e:
        print(Error(f"Unexpected error: {e}", f"{type(e).__name__}"))
