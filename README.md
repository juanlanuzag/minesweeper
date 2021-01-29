# Minesweeper

![image alt](https://cdn.discordapp.com/attachments/691835456534609950/804542001277173829/unknown.png)

## Relevant Links
- API root: http://ec2-18-191-99-146.us-east-2.compute.amazonaws.com:8080/api/
- API documentation: http://ec2-18-191-99-146.us-east-2.compute.amazonaws.com:8080/swagger-ui/
- Frontend: http://minesweeper-frontend.s3-website.us-east-2.amazonaws.com/#/

## What was built?
This project is a web-based minesweeper game app using Python, Django, django rest framework, Swagger, SQLite, VueJs and AWS (EC2 and S3).
All the development process involved making:
- Game logic
- Game persistence layer
- Game API
- API Documentation
- Game frontend
- Deploying the app to AWS

## Design decisions

#### Persistence and business logic

Since I wasn't very sure on what was the good way to persist the game status,
I decided to decouple the game logic from the way it's persisted.
By doing so, the persistence layer can be changed without having to redo the logic.

In the business logic layer, each minesweeper game stores the game parameters
(number of rows, columns and mines), if it's currently won or lost and the board status.
The board is a list of lists of cells and each cell knows if it has a mine or not and
if it was revealed or flagged.

Now thinking about persistence, I considered storing games in a document-based database.
This is because each game is an entity that will not be accessed
through complex queries (by id and probably in the future by owner, but not much more)
and its internal representation has a list of lists of cells
(great to store in a document but no so much in a SQL database).
However, since I'm using Django and DRF, I decided to store it in an SQL database for simplicity, while maintaining the possibility to change the persistence layer easily.

## To run the project

For the backend:
```
cd back/
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

For the frontend:
```
cd front/minesweeper/
npm install
npm run serve
```
