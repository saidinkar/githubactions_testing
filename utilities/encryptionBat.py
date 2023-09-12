import base64


def encoding(Variable):
    sample_string_bytes = Variable.encode("ascii")
    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")
    print(f"Encoded string: {base64_string}")


var = input('Enter the password to be encrypted: ')
encoding(var)
