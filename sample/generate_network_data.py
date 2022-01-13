import csv
import argparse


def main(num_rows: int, prefix: str, first_octet: int, second_octet: int, third_octet: int):
    host_data = generate_host_data(prefix, first_octet, second_octet, third_octet, num_rows)
    write_file(host_data)


def generate_host_data(prefix: str, first_octet: int, second_octet: int, third_octet: int, rows: int, obj_type="Host"):
    host_data = ["NAME,DESCRIPTION,TYPE,VALUE,LOOKUP"]
    fourth_octet = 1
    for num in range(1, rows):
        ip_address = f"{first_octet}.0.{third_octet}.{fourth_octet}"
        host_data.append(f"{prefix}-{ip_address},Test {obj_type} Object {ip_address},{obj_type},{ip_address},")
        fourth_octet += 1
        if fourth_octet == 256:
            third_octet += 1
            fourth_octet = 1
            if third_octet == 256:
                second_octet += 1
                third_octet == 1
                if second_octet >= 256:
                    raise ValueError
    return host_data


def write_file(data, filename="test_data.csv"):
    with open(filename, mode="w") as data_file:
        for line in data:
            data_file.writelines(f"{line}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("-r", "--rows", default=1000, dest="num_rows", help="Number of rows to create", type=int)
    parser.add_argument(
        "-p",
        "--prefix",
        default="test",
        dest="prefix",
        help="The prefix of the generated object name. ",
        type=str,
    )
    parser.add_argument(
        "-f",
        "--firstoctet",
        default=10,
        dest="first_octet",
        help="The First octet of the generated IP address",
        type=int,
    )
    parser.add_argument(
        "-s",
        "--secondoctet",
        default=0,
        dest="second_octet",
        help="The initial second octet of the generated IP address",
        type=int,
    )
    parser.add_argument(
        "-t",
        "--thirdoctet",
        default=0,
        dest="third_octet",
        help="The initial third octet of the generated IP address",
        type=int,
    )
    args = parser.parse_args()

    # TODO add option for filename/path
    main(args.num_rows, args.prefix, args.first_octet, args.second_octet, args.third_octet)
