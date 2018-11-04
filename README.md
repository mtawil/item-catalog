# Item Catalog

This project has been developed so you can be able to create items like (notes, documents, articles ..ect) with the reserved categories.

## Getting Started

These instructions will help you out to run this project on your local machine.

### Prerequisites

Just download and install Python3, if you haven't install Python3 before, please follow [the instructions to install it](https://realpython.com/installing-python/).


### Installing

1. Clone this repo:

```sh
$ git clone https://github.com/mtawil/item-catalog.git item-catalog && cd item-catalog
```

2. Configure Google sign-in by opening `config/passport.py`, change the consumer_key & consumer_secret. [Create it](https://developers.google.com/identity/protocols/OAuth2WebServer#creatingcred) if you don't have one.

3. Install the project requirements:

```sh
$ pip3 install -r requirements.txt
```

4. Create database tables and insert category records:

```sh
$ python3 db.py migrate --seed --path database/migrations --seed-path database/seeds
```

You can use the following command if you want to refresh the database:

```sh
$ python3 db.py migrate:refresh --seed --path database/migrations --seed-path database/seeds
```

## Running the application

Run the application:
```sh
$ python3 main.py
```

> If you want to disable the application debug: `$ export FLASK_DEBUG=0`

Open [http://localhost:5000](http://localhost:5000) from your browser.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

This project use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/mtawil/item-catalog/tags). 

## Authors

* **Mohammad AlTaweel** - *Initial work* - [mtawil](https://github.com/mtawil)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
