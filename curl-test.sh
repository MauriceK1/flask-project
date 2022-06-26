#!/bin/sh

read -p 'ENTER NAME: ' NAME
read -p 'ENTER EMAIL: ' EMAIL
read -p 'ENTER MESSAGE: ' CONTENT

if curl -X POST -d 'name='$NAME'&email='$EMAIL'&content='$CONTENT'' http://localhost:5000/api/timeline_post; then 
    echo "Successfully added post" 
fi

curl http://localhost:5000/api/timeline_post  

