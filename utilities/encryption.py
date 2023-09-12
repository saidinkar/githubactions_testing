import base64


def encode(Variable):
    sample_string_bytes = Variable.encode("ascii")
    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")
    print(f"Encoded string: {base64_string}")
    return base64_string


def decode(Variable1):
    newpass = Variable1.encode("ascii")
    sample_stringnew = base64.b64decode(newpass)
    sample_stringnew1 = sample_stringnew.decode("ascii")
    return sample_stringnew1
