import os
import requests

CHAVE = os.environ["AI_GATEWAY_API_KEY"] # a chave vem do segredo, não do código
URL = "https://ai-gateway.vercel.sh/v1/chat/completions"
MODELO = "google/gemini-3.5-flash-lite"

INSTRUCAO = ("Você é um tutor paciente que explica tecnologia para jovens, "
 "em português do Brasil, com frases curtas.")


def perguntar(pergunta):
 resposta = requests.post(
 URL,
 headers={
 "Authorization": f"Bearer {CHAVE}",
 "Content-Type": "application/json",
 },
 json={
 "model": MODELO,
 "messages": [
 {"role": "system", "content": INSTRUCAO},
 {"role": "user", "content": pergunta},
 ],
 "temperature": 0.7,
 },
 timeout=60,
 )
 if resposta.status_code == 401:
    return "Chave inválida ou expirada. Confira o segredo AI_GATEWAY_API_KEY."
 if resposta.status_code == 402:
    return "O limite de gasto da sua chave acabou. Fale com o professor."
 if resposta.status_code == 429:
    return "Muitos pedidos ao mesmo tempo. Espere um pouco e tente de novo."
 resposta.raise_for_status()
 dados = resposta.json() # transforma o JSON em dicionário
 return dados["choices"][0]["message"]["content"]


print(perguntar("O que é computação em nuvem?"))

