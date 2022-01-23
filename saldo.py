from helper import *


def main():
    action = pathlib.Path(sys.argv[0]).stem
    if action == "saldo" and len(sys.argv) == 4:
        manager.transform_data()
        manager.execute(action, sys.argv[2], sys.argv[3])
        manager.write_data_to_file(sys.argv[1])
        # manager.print_info("saldo plik")
        manager.execute("konto")


main()


