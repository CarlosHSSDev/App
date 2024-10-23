def read_users_file():
    try:
        with open("assets/Users.txt", "r+", encoding="utf-8") as file:
            content = file.read().strip()
            if content:
                users = [user.split(";") for user in content.split("||")]
                return users
            return []
    except FileNotFoundError:
        print("Arquivo de usuários não encontrado!")
        return []
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return []

class User:
    def __init__(self, email, senha, nome=None):
        self.nome = nome
        self.email = email
        self.senha = senha

    def login(self):
        users = read_users_file()
        for user in users:
            try:
                if self.email == user[1] and self.senha == user[2]:
                    print("Login feito com sucesso!")
                    return 200
            except IndexError:
                print("Erro ao acessar os dados do usuário.")
                return 500
        print("Credenciais incorretas.")
        return 401

    def cadastro(self):
        users = read_users_file()
        for user in users:
            if self.email == user[1]:
                print("Usuário já existe.")
                return
        
        with open("assets/Users.txt", "a", encoding="utf-8") as file:
            separator = "" if not users else "||"
            file.write(f"{separator}{self.nome};{self.email};{self.senha};")
            print("Usuário cadastrado com sucesso!")
            return 200
        
