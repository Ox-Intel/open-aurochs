# Aurochs

Aurochs is the foundational codebase for the Ox product.  It supercedes [client](https://github.com/Ox-Intel/client), [service](https://github.com/Ox-Intel/service), [compose](https://github.com/Ox-Intel/compose), and [e2e](https://github.com/Ox-Intel/e2e).


## Long-term Roadmap

- ✅ Provide versioned data across the app, with the ability to rollback, fork, and clone at any point in history.
- ✅ Transition from the react-based client (`apps/client`) to a vue-based front-end (`apps/webapp`)
- Create data vaults, allowing scores to exist independently of scorecards, and creating a robust way for clients to integrate their own data silos.


## Running the codebase

1. Copy `env.sample` to `.env`, and adjust as needed.

2. Set up FontAwesome Pro (see below).

3. Run

```bash
docker compose up --build
docker compose run aurochs bash -c "python3 manage.py migrate"
```

4. Open [http://localhost:8120](http://localhost:8120)

### FontAwesome Pro

This project uses [FontAwesome Pro](https://fontawesome.com/plans) icons (duotone style). You'll need a FontAwesome Pro license to build the frontend.

1. Get your npm token from [fontawesome.com/account](https://fontawesome.com/account)
2. Add it to your `.env` file:
   ```
   FONTAWESOME_NPM_TOKEN=your-token-here
   ```
3. Install frontend dependencies:
   ```bash
   cd aurochs/apps/webapp
   yarn install
   ```

The token is read by `.yarnrc.yml` during `yarn install` to authenticate with the FontAwesome npm registry.

### Issues building?

Here's a few standard debugging steps:

Run migrations:

```bash
docker compose run aurochs bash -c "python3 manage.py migrate"
```

Warm the cache:

```bash
docker compose run aurochs bash -c "python3 manage.py warm_cache"
```

Clear the cache:

```bash
docker compose run aurochs bash -c "python3 manage.py clear_cache"
```

Try a fresh build:

```bash
docker compose build --no-cache
```

## Running the test suite locally.

To run in-container:

```bash
docker compose run aurochs pt
```

To run in your local system (assumes you've `pip install`ed):

```bash
POSTGRES_HOST=localhost pt
```

To run continuously, for development:

```bash
docker compose run --rm aurochs bash -c 'watchmedo shell-command --patterns="*.py" --recursive --command="python manage.py test --settings=aurochs.envs.test --noinput"'
```

## Using the admin site.

Navigate to `/administration` to use the django admin site, and log in with a user that has been set (via the shell) with `is_superuser = True`. No other users will work, and there are intentionally no codebase paths to set users as superusers.

## Running e2e

We use Cypress: https://docs.cypress.io
We also use a library for screenshot-testing, in a few cases: https://github.com/jaredpalmer/cypress-image-snapshot, with a recent re-fork for cypress 10: @simonsmith/cypress-image-snapshot

Prerequisites: `npm i -g cypress @simonsmith/cypress-image-snapshot`

1. Spin up the local system: `docker compose up`
2. Prepopulate the database with the e2e accounts: `docker compose run aurochs bash -c "python3 manage.py setup_e2e_accounts"`
3. Run cypress `sudo cypress open`

### Generating e2e screenshots.

If we've made significant changes to the app, and our screenshot-based e2e tests are failing, you can regenerate them.

1. `sudo rm -rf cypress/snapshots`
2. `sudo cypress run  --browser chrome --spec cypress/e2e/*screenshot.spec.js`    (If this fails on `input`, make sure you've run `setup_e2e_accounts`.)
3. Check in the changes and push, and make sure things pass on CI.

Note: If you make new e2e tests that use `matchImageSnapshot`, please name them ending in `screenshot.spec.js`

### Cleaning up e2e

E2e tests generate a lot of (org-namespaced) data in the local database.  If they're failing, they can leave behind artifacts.  The following command will do a quick cleanup of those artifacts.

`docker compose run aurochs bash -c "python3 manage.py cleanup_e2e_data"`

## Using the admin site.

Navigate to `/administration` to use the django admin site, and log in with a user that has been set (via the shell) with `is_superuser = True`. No other users will work, and there are intentionally no codebase paths to set users as superusers.

## Getting authorized querysets.

Aurochs uses standard django patterns, but with our own per-object permissions system. To use it, call:

```python
Model.authorized_objects.authorize(user=request.user)
```

This will return a standard django queryset, filtered and permissioned. All normal methods, `.filter()`, `.create()`, `.delete()` etc will all work.

If you need to bypass the permission system, there are a few other managers.

```python
Model.objects - returns a raw django queryset, excluding deleted objects.
Model.objects_with_deleted - returns a raw django queryset, including deleted objects.
Model.raw_objects - returns a raw django queryset.  (This should be used very sparingly.)
```

## Managing image uploads.
We use [django-binary-database-files](https://github.com/kimetrica/django-binary-database-files) for maximum portability.  It has a couple of management commands that can periodically be useful.

`python manage.py database_files_cleanup`  will clear all the unused images from the database and file system.

`python manage.py database_files_dump` will drop all the database files to the file system, for faster serving.


## Developing locally.

If you don't want to build the JS files within the docker containers, you can build locally using:

**Vue Webapp**: `cd apps/webapp && yarn watch`
**Public Webapp**: `cd apps/public && yarn watch`

### Toggling between public and airgapped.
In your `.env` file, set: `AIRGAPPED=True` to test the airgapped environment.  If the variable is missing or False, the public site will be included.

## Migrating the current database. (for dev)

1. Export from production: `docker exec -i 123123124123 /bin/bash -c "PGPASSWORD=postgres pg_dump --username postgres dev_service_db --disable-dollar-quoting --column-inserts --quote-all-identifiers" > ./dump2022-mm-dd.sql`
2. Update the schema: `sed 's/public"."/public"."legacy_/g' dump.sql > dump-new.sql`
3. Spin up an instance locally, create the aurochs database. (If you have a db locally you want to wipe, just delete the `postgres-data` folder, and then `docker compose up --build`)
4. Migrate and set up schema. `docker compose run aurochs bash -c "python3 manage.py migrate"`
5. Import to legacy tables. `psql -U postgres -h localhost aurochs < dump-new.sql `
6. Run the setup command. `docker compose run aurochs bash -c "python3 manage.py initial_setup"`

## Migrating the current database. (for heroku prod)

1. Follow all of the dev steps above, after starting with a completely blank database.
2. Export locally: `docker exec -i 123123124123 /bin/bash -c "PGPASSWORD=postgres pg_dump --username postgres aurochs -Fc" > ./dump2022-mm-dd.migrated.sql`
3. Upload this to the database s3 bucket.
4. Share with a presigned url for 10 minutes from the AWS console.
5. `export URL=https://presigned-url`
6. `heroku pg:backups:restore $URL DATABASE_URL --app ox-production`
7. `heroku run python manage.py migrate --app ox-production` (Should note all migrations are done.)

## Deployment to Heroku

- `development` will be deployed automatically to `ox-staging`, at https://future.oxintel.ai (in the future this will be staging.oxintel.ai)
- `production` will be deployed automatically to `ox-production`, at https://app.oxintel.ai

### Cloning Production to staging

```
# Capture a new backup
heroku pg:backups:capture -a ox-production

# Run, note the latest backup ID, e.g. b00x
heroku pg:backups -a ox-production

heroku pg:backups:restore ox-production::b000 DATABASE_URL --app ox-staging
```

## Deployment to Airgapped systems.

We have an automated build process to generate minimized, gzipped images ready for delivery.  To kick it off:
1. `git tag v1.xx production`
2. `git push origin --tags`
3. Wait for the [generate release package](https://github.com/Ox-Intel/aurochs/actions/workflows/release.yaml) action to complete on github.
4. Log into our AWS S3 console, and download, or generate a secure link for the release file.

### Config

We run with:

- Heroku Postgres (Standard or higher)
- Heroku Redis (Standard or higher)
- `heroku config:set DISABLE_COLLECTSTATIC=1`
- `heroku config:set ENV=live`
- `heroku redis:maxmemory REDIS_URL --policy allkeys-lru  -a APP_NAME`
- Heroku buildpacks:

1. heroku/nodejs
2. heroku/python
3. https://github.com/Ox-Intel/heroku-buildpack-run.git

- **Note**, while we're still using the `client` codebase, it's necessary to run `cd ./aurochs/apps/client/client && yarn && yarn build-single` locally, and commit changes to `dist`, so we don't have to do the very slow build during deployment.

## Code Style

### Python

We use `black` and `flake8` to maintain our style.

To auto-format:
```bash
black aurochs
```

### JavaScript
We use Prettier and eslint to maintain our style.

To auto-format
```bash
yarn cleanup
```
