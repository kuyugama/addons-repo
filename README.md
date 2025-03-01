# Addon-Repo

This is repository for python addons written to use with `addon-system` and baked by `pybaked` libraries

> All uploaded can be downloaded

This repository allows you to download all addons that was uploaded to it
(except deleted addons, they are deleted completely).
It also supports addon encrypting natively using AES-GCM encryption algorithm.
So, your addons is safe(just joking, safe places doesn't exist) to store here, 
because even if users would download it - access its 
content would be problematic.

## Host own instance of Addon-Repo

Update PostgreSQL url in `secrets.example.yaml` file
and rename it to `.secrets.yaml`

### Using docker

1. Change PostgreSQL credentials in `example.env` file and rename it to `.env`

2. Run

```bash
docker compose up
```

Server will be exposed at 8000 port by default.
To expose it on custom port change `APP_PORT` value in your `.env` file

### Manually

1. Set-up PostgreSQL

2. Install uv:
    ```bash
    pip install uv
    ```

3. Install dependencies:
    ```bash
    uv sync
    ```
4. Apply database migrations:
   ```bash
   alembic upgrade head
   ```

5. Install uvicorn:
    ```bash
    uv pip install uvicorn
    ```

6. Run:
    ```bash
    uvicorn main:app
    ```

# Details

## Why
My purpose was to make place where addons can be stored(addons from `addon-system` library). 
Also, this place must support encryption to safely store addons files.

## Storing addons
Addons are stored in .py.baked format(from `pybaked` library). 
And can be encrypted using AES encryption to ensure safety of addon's content

## Addon encryption
Addons are encrypted using AES-GCM encryption with dynamic keys generation.
Each version of addon is encrypted using its own encryption key, 
this key is generated once version is published and encrypted with 
addon's owner's public key, so only owner can get this key to decrypt addon file.

After encryption addon file has the following structure:
```
[IV 12 bytes] [Encrypted content, batch size 64 kb] [authentication tag, 16 bytes]
```

## Authorization
To authorize you need to provide RSA public key
(size: 2048, exponent: 65537) serialized using DER format 
with SubjectPublicKeyInfo standard encoded using base64.

**Authorization example**:

Sign-up

`POST` `/auth/signup`
```json
{
   "nickname": "YourNicknameInRepo",
   "secret": "YourPasswordInRepo",
   "public_key": "YourBase64EncodedPublicKey"
}
```
Sign-in

`POST` `/auth/signin`
```json
{
   "nickname": "YourNicknameInRepo",
   "secret": "YourPasswordInRepo"
}
```

In both endpoint you get `Token` response:
```json
{
   "secret": "TokenBody",
   "_expires": "Token expiration date timestamp",
   "expires": 123123123,
   "_created": "Token creation date timestamp",
   "created": 123123123,
   "_updated": "Token last update date timestamp",
   "updated": 123123123,
   "id": 123
}
```
> Note: I use fields starting with _ as comments and these fields don't exist on real responses

> I think, authorization is the only hardest thing in usage  
> To get all endpoints and its examples see https://addons-repo.nyam.online/docs
