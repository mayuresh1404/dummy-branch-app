#!/bin/bash

echo "🚀 Setting up Branch Loan API..."

# Create directories
mkdir -p nginx/ssl logs

# Generate SSL certificate
if [ ! -f nginx/ssl/branchloans.key ]; then
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout nginx/ssl/branchloans.key \
        -out nginx/ssl/branchloans.crt \
        -subj "/C=IN/ST=Maharashtra/L=Mumbai/O=Branch/OU=DevOps/CN=branchloans.com"
    echo "✅ SSL certificate generated"
fi

# Add domain to hosts file
if ! grep -q "branchloans.com" /etc/hosts 2>/dev/null; then
    echo "127.0.0.1 branchloans.com" | sudo tee -a /etc/hosts
    echo "✅ Added branchloans.com to /etc/hosts"
fi

# Create .env
cp .env.development .env 2>/dev/null || true

echo "✅ Setup complete!"
echo ""
echo "Next: Run 'docker-compose up -d'"