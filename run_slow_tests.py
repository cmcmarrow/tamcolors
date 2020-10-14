from tamcolors.tests import all_tests


def main():
    exit(int(not all_tests.tests_main(True)))


if __name__ == "__main__":
    main()
