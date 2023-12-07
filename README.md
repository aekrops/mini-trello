# Mini Trello
## “Mini Trello/Kanban” interface - With Drag &amp; Drop of cards between columns

### Steps to run application:
- `docker compose build` or `docker-compose build`
- `docker compose up -d db`
- run `backend/test_create_table.py` for table creation
- `docker compose up -d`

Also add the `.env` file to backend folder
#
You can just copy it 
````
DYNAMODB_ENDPOINT_URL=http://localhost:8000
AWS_ACCESS_KEY_ID=dummy
AWS_SECRET_ACCESS_KEY=dummy
AWS_REGION_NAME=eu-west-1
SECRET_KEY=django-insecure-xv5$bj&)bb$rcj6w03bp$u=0#h^pga4gagel0f+4vw-=e54rw%
DEBUG=True
````

