from security import export_key, generate_keys


# Check if we have locally stored keys or generate new ones
def check_key(keyfile):
    try:
        key = open(keyfile, 'r')
    except Exception:
        return None
    else:
        return key


def main():
    if check_key('private_key.pem') is None or \
            check_key('public_key.pem') is None:
        privatekey, publickey = generate_keys()
        export_key(privatekey, private=True)
        export_key(publickey)


if __name__ == '__main__':
    main()
