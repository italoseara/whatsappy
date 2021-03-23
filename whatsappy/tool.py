def error_log(error):
    print(error)

    with open('error.log', 'a+') as f:
        f.writelines(f'[ERROR] {error}')
        f.writelines('='*100 + '\n')