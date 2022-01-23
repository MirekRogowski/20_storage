from helper import *


def main():
    action = pathlib.Path(sys.argv[0]).stem
    if action == "sprzedaz" and len(sys.argv) == 5:
        manager.transform_data()
        manager.execute(action, sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
        # print(manager.error[0])
        manager.write_data_to_file(sys.argv[1])
        # manager.print_info("sprzedaz")
        manager.execute("konto")


main()
