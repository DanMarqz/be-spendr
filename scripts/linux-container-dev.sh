docker build -t be-spendr \
    --build-arg PORT=$PORT \
    --build-arg VERSION=$VERSION \
    --build-arg TOKEN=$TOKEN \
    --build-arg APP_SECRET_KEY=$APP_SECRET_KEY \
    --build-arg DB_URI=$DB_URI \
    --build-arg DB_NAME=$DB_NAME \
    --build-arg ERROR_MSG=$ERROR_MSG \
    --build-arg DEBUG=$DEBUG \
    .

docker run -d --name be-spendr -p 5000:5000 be-spendr