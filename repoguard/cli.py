import argparse

def main():
    parser=argparse.ArgumentParser(prog="repoguard")
    subparser=parser.add_subparsers(dest="command")

    subparser.add_parser("validate")

    args=parser.parse_args()

    if args.command=="validate":
        print("Repoguard validate running")
    else:
        parser.print_help()