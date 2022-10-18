


def is_template_message(text):
    return text.startswith("{№")

def get_position_from_template_message(text):
    try:
       return int(text[2])   
    except:    
       return 0

print(is_template_message('{№1} {№язева 67 - му.'))
print(get_position_from_template_message('{№1} {№язева 67 - му.'))