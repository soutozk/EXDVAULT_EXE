import hashlib
import requests


def check_password_pwned(password: str) -> bool:
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix = sha1[:5]
    suffix = sha1[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"

    res = requests.get(url, timeout=5)

    if res.status_code != 200:
        raise Exception("Erro na API")

    hashes = (line.split(":") for line in res.text.splitlines())

    return any(h == suffix for h, _ in hashes)


# ----------------------------
# TESTE ISOLADO
# ----------------------------

if __name__ == "__main__":
    senha = "123456Aa@#"

    print("Testando senha:", senha)

    try:
        if check_password_pwned(senha):
            print("🚨 SENHA VAZADA")
        else:
            print("✅ Senha não encontrada")

    except Exception as e:
        print("Erro ao acessar API:", e)