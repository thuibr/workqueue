def hello(*args, **kwargs):
    if len(args) > 0:
        msg = f"hello, {args[0]}"
    else:
        msg = "hello"

    if kwargs["all_caps"]:
        msg = msg.upper()

    print(msg)
