README
======

Intro
-----
The project from which this task is derived consists of several services that are being run
behind a reverse proxy. Some of these services are available to the external clients, whilst
some of them are fully hidden and available only on the private network (traffic from service to service), but still having some
endpoints available beyond. All of that is guarded mostly by Nginx routing rules, but
the development team wanted to have extra security layer, if the reverse proxy would get misconfigured.

Task
----

The task is to create a middleware compatible with Falcon framework (v1.4.1, Python 3.8.1)
that will be authorizing incoming requests based on matching an API key in the header
to the challenge key set in the project settings.

Header `Authorization: Apikey {token}` must match `settings.API_KEY`.

The middleware must provide some form of configuration, because some of the endpoints must
require such authorization, and some other should just pass the requests.

Also you need to take into account `Bearer` token authentication.

At this moment the app has 5 endpoints:

- `/auth/register` - no authorization required
- `/user/whoami` - no authorization required, but session token required (`Bearer`)
- `/collections` - no authorization required
- `/internal/users` - `Apikey` must be provided
- `/internal/collections` - `Apikey` must be provided

So for example a header giving access to `/internal/collections`
will look like: `Authorization: Bearer user-session, Apikey ILoveKittens`.
(Note that `user-session` is valid, hardcoded input)

If the authorization does not pass the app should return `403 Forbidden`

For the above requirements unit tests where created. The solution must pass all of them.

Attention: the task has also a second stage where the requirements change a bit, try to
create your solution such, that it will be agile for the future requirements.
Also there are few additional tests which test against common mistakes, or _cheaty_ solutions
on a different branch ;)

Run the environment

-------------------
`docker-compose up` & `docker exec -it api bash`, but virtual env should also be sufficient.

in the container you can run `invoke format` which formats the code.

Run the tests
-------------

running `pytest` in the container will run all the tests cases including `mypy` & `flake8`,
Note that the tests are hardcoded at the `core/` level - this example app does not implement it.
