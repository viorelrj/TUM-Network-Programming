# Network Programming Labs

## Student Notes
Written for python 3

Uses:
* `threading`
* `Queue`

## Lab Instructions

1. Pull a docker container (alexburlacu/pr-server) from the registry

2. Run it, don't forget to forward the port 5000 to the port that you want on the local machine

3. Only languages and libraries supporting threads, locks, and semaphores are allowed. Node or JS generally and Elixir/Erlang are prohibited. Go and Rust are allowed but with some constraints. Discuss with me the implementation.

4. Now that you're up and running, you need to access the root route of the server and find your way to /register

5. The access token that you get after accessing the /register route must be put in a HTTP header of the subsequent requests under the key X-Access-Token key

6. Most routes return a JSON with data, data type, and link keys. Extract data from data key and get next links from link key

7. Hardcoding the routes is strictly forbidden. You need to "traverse" the API

8. Access token has a timeout of 20 seconds, and you are not allowed to get another token every time you access a different route. So, one register per program run

9. Once you fetch all the data, convert it to a common representation, doesn't matter what this representation is

10. The final part of the lab is to make a concurrent TCP server, serving the fetched content, that will respond to (mandatory) a column selector message, like `SelectColumn column_name`, and (optional) `SelectFromColumn column_name glob_pattern`

11. All the code must be on GitHub with a readme file explaining how to launch the project and implementation/tasks done


Optional tasks:
- `SelectFromColumn column_name glob_pattern` message for TCP server
- Implementing your own thread pools
- Dispatching data to a different process pool/dedicated processes for conversion while the fetching is running (can use queue)
- Anything else, turn on your imagination


Grading policy:
- -0.5 to -2 for badly written code (formatting, coupling, alignment with language conventions), can be slightly alleviated if having optional features
- if the required functionality is not implemented, in the required way, the lab is invalid - no grade
- if you are late one week, you are subtracted one point. Still, you can recover it by implementing some optional features
- if you want to be sure you'll get a 10, implement some optional features (1 simple or 2 harder ones)
- if the lab is plagiarized, therefore more than 30% of it is not done by you, you can still get a 5 if you at least know how the code works. If you don't, guess what will happen 😉
