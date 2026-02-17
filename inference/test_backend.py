from inference.verify import verify_signature

with open("sample1.png", "rb") as f1, open("sample2.png", "rb") as f2:
    output = verify_signature(f1.read(), f2.read())
    print(output)
