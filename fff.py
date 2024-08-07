



def get_upload_to(func):
    def wrapper(*args, **kwargs):
        return func
    
    
    return wrapper


@get_upload_to
def haha(count):
    print(count)
    return


haha(1)(1)