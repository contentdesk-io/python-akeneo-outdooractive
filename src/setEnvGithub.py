import requests
import json
from base64 import b64encode
from nacl import encoding, public
from os import getenv
from dotenv import find_dotenv, load_dotenv
import glob

load_dotenv(find_dotenv())

GITHUB_TOKEN = getenv('GITHUB_TOKEN')
GITHUB_OWNER = getenv('GITHUB_OWNER')
GITHUB_REPO = getenv('GITHUB_REPO')

def encrypt(public_key: str, secret_value: str) -> str:
  """Encrypt a Unicode string using the public key."""
  public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
  sealed_box = public.SealedBox(public_key)
  encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
  return b64encode(encrypted).decode("utf-8")

def setHeaders(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github+json',
    }
    return headers

def createEnvironment(owner, repo, token, environment):
    headers = setHeaders(token)
    response = requests.put(f'https://api.github.com/repos/{owner}/{repo}/environments/{environment}', headers=headers)
    print(f'Created environment {environment}: {response.status_code}')
    print(response.text)

def getPublicKey(owner, repo, token, environment):
    headers = setHeaders(token)
    response = requests.get(f'https://api.github.com/repos/{owner}/{repo}/environments/{environment}/secrets/public-key', headers=headers)
    publicKey = response.json()
    print(f'Public key: {publicKey}')
    return publicKey

def createEncryptSecret(owner, repo, token, environment, secretName, secretValue, publicKey):
    headers = setHeaders(token)
    encrypted_secret = requests.put(f'https://api.github.com/repos/{owner}/{repo}/environments/{environment}/secrets/{secretName}', headers=headers, data=json.dumps({
            'encrypted_value': secretValue,
            'key_id': publicKey['key_id'],
        }))
    print(f'Added secret to {environment}: {encrypted_secret.status_code}')
    print(encrypted_secret.text)
    print(f'Secret {secretName} added to {owner}/{repo}')

def loadDotEnv():
    # Find all .env.xxx files
    env_files = glob.glob('.env.*')

    # Print the list of files
    print(env_files)
    

def main():
    # Personal Access Token
    token = GITHUB_TOKEN

    # Repository details
    owner = GITHUB_OWNER
    repo = GITHUB_REPO

    # Headers
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github+json',
    }

    # Environments to create
    environments = ['test1', 'test2', 'test3']

    # Create environments
    # https://docs.github.com/de/rest/deployments/environments?apiVersion=2022-11-28#create-or-update-an-environment
    for env in environments:
        createEnvironment(owner, repo, token, env)

    # Secret to add
    secret_name = 'MY_SECRET'
    secret_value = 'secret_value_here'

    # Add secret to environments
    # https://docs.github.com/de/rest/guides/encrypting-secrets-for-the-rest-api?apiVersion=2022-11-28#example-encrypting-a-secret-using-python
    for env in environments:
        publicKeyEnv = getPublicKey(owner, repo, token, env)
        print(f'Public key: {publicKeyEnv}')

        secretValue = encrypt(publicKeyEnv['key'], secret_value)

        print(f'Adding secret to {env}')
        createEncryptSecret(owner, repo, token, env, secret_name, secretValue, publicKeyEnv)

if __name__ == '__main__':
    loadDotEnv()
    #main()