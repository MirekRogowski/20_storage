from helper import *


def main():
    action = pathlib.Path(sys.argv[0]).stem
    if action == "konto" and len(sys.argv) == 2:
        manager.transform_data()
        manager.execute(action)


main()
