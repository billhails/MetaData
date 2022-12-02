import secrets

def generate_dotenv(architecture):
    with open('architectures/' + architecture + '/.env', "w") as fh:
        fh.write('# generated by the application, you should make sure this file is ignored by git\n')
        fh.write(f'ACCESS_TOKEN_SECRET={secrets.token_hex(64)}\n')
        fh.write(f'REFRESH_TOKEN_SECRET={secrets.token_hex(64)}\n')
