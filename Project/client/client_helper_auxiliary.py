def check_address(address):
    """Function to check if address is valid. valid address format ex: 1.1.1.1:1234"""
    if len(address.split(":")) == 2:
        values = address.split(":")
    else:
        return False

    first = values[0]
    second = values[1]

    if not len(first.split(".")) == 4:
        return False  # check far ip by checking for 3 .
    try:
        second = int(second)  # make sure second part is an int
    except ValueError:
        return False

    return first, second


def ensure_address(client_helper, temp):
    address = check_address(temp)  # convert address to str int tuple
    while not address:  # check for valid format
        client_helper.log(f"{temp} is an invalid address")
        temp = client_helper.read("Enter valid address (e.g 127.0.0.1:6000): ")
        address = check_address(temp)
    return address
