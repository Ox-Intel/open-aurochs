# Ox Intel Application Install Instructions

## Initial Installation

These instructions provide the set of commands needed to install the Ox Intel application.

The installation process will install the needed Docker images, create a Docker network, start the database
and application services and configure the application.

To start copy the installation package to a working directory where the files can be maintained (.e.g /svr)

Next, you will need to expand the archive by running the following command:

```commandline
tar -xvf <NAME OF UPDATE>
```

When this process is complete, a directory will be created with the same name as the update file. To see this run the
following command:

```commandline
ls
```

Now change directories into that directory:

```commandline
cd <NAME OF DIRECTORY>
```

Next, we will run the installation script. To do this run the following command:

```commandline
 sudo ./setup-aurochs.sh
```

To verify the update navigate to the application url and login.

## Upgrades

To upgrade an existing installation of Ox, use the following steps:

Copy the installation package to a working directory where the files can be maintained (.e.g /svr)

Next, you will need to expand the archive by running the following command:

```commandline
tar -xvf <NAME OF UPDATE>
```

When this process is complete, a directory will be created with the same name as the update file. To see this run the
following command:

```commandline
ls
```

Now change directories into that directory:

```commandline
cd <NAME OF DIRECTORY>
```

Next, we will run the installation script. To do this run the following command:

```commandline
 sudo ./update-aurochs.sh
```
