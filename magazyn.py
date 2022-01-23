from helper import *


def main():
    action = pathlib.Path(sys.argv[0]).stem
    if action == "magazyn" and len(sys.argv) >= 3:
        manager.transform_data()
        manager.execute(action, sys.argv[2:])
        manager.execute("konto")


main()
