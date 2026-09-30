# Book Shop Postman Collection

Import `BookShop.postman_collection.json` and `BookShop.postman_environment.json` into Postman.

Run the requests in this order for the smoothest setup:

1. `Users / Register`
2. `Users / Login`
3. `Authors / Create Author`
4. `Categories / Create Category`
5. `Books / Create Book`
6. `Comments / Create Comment`
7. `Saved / Create Saved`

The login request stores `accessToken` in the environment. The create requests also store the latest IDs so the follow-up detail/update/delete requests can be run directly.

Author and category deletes will return `409 Conflict` while books still reference them. Delete the dependent book first if you want to exercise those endpoints successfully.

Swagger UI is available at `http://127.0.0.1:8000/docs` after the app is running.
