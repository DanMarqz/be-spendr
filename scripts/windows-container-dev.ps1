docker build -t be-spendr `
    --build-arg PORT=$env:PORT `
    --build-arg VERSION=$env:VERSION `
    --build-arg TOKEN=$env:TOKEN `
    --build-arg APP_SECRET_KEY=$env:APP_SECRET_KEY `
    --build-arg DB_URI=$env:DB_URI `
    --build-arg DB_NAME=$env:DB_NAME `
    --build-arg ERROR_MSG=$env:ERROR_MSG `
    --build-arg DEBUG=$env:DEBUG `
    .

docker run -d --name be-spendr -p 5000:5000 be-spendr