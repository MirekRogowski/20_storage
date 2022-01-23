from helper import *


def main():
    action = pathlib.Path(sys.argv[0]).stem
    if action == "przeglad" and len(sys.argv) == 4:
        manager.transform_data()
        manager.execute(action, int(sys.argv[2]), int(sys.argv[3]))
        manager.execute("konto")


main()

