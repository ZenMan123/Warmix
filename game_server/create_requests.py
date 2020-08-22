def create_requests(command, *args):
    arr = [command] + list(args)
    return '%'.join(arr)