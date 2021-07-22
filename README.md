# Launch Twitter

This app uses GPT-3 to auto-generate content based on famous tweets.

## Running locally

Create a new virtual environment

```
python3 -m venv venv
source venv/bin/activate
```

Install requirements

```
pip install -r requirements.txt
```

Create .env file and fill keys found in .env.sample
```
cp .env.sample .env    
```

Run

```
gunicorn api:app
```
## Deployment
This app is currently hosted on [Railway](https://railway.app/) and is redployed with every push to the repo. API can be accessed via https://launch-twitter-backend-production.up.railway.app/api/v1/ping