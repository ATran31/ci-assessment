# Install server dependencies

```bash
# Create a virtual environment (Optional)
python -m venv <virtual-env-name>

pip install -r requirements.txt
```

> Note: The server will use boto3 to access AWS S3 resources and assumes you have valid configured AWS permissions at `~/.aws/credentials` or in the enviornment variabes.

# Install UI dependencies

Install npm dependencies

```bash
cd ui
npm install
```

# Build UI.

```bash
npm run build
```

# Starting the local server

```bash
uvicorn main:app --reload --port 3000
```

Go to localhost:3000.
