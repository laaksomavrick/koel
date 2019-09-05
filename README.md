# koel

Koel sends an sms message within the nearest half hour to specified phone numbers
whenever a weather alert occurs on the Government of Canada's weather alert rss feed for a specified
city.

I developed this tool to tinker with Python and various AWS offerings, alongside using cloudformation for infrastructure-as-code.
The python code runs in a lambda function, triggered every 30 minutes by a cloudwatch event, storing message history in a s3 bucket.

## What is a koel?

The Pacific koel *(Eudynamys orientalis)*, also known as the eastern koel, is a species of cuckoo 
in the Cuculidae family. In Australia, it is colloquially known as the rainbird or stormbird, as 
its call is usually more prevalent before or during stormy weather.

## How do I get this running for myself?

Prerequisites:
  * A computer running macOS (`zip` is used in `scripts/deploy.sh`)
  * A properly configured `aws` cli installed on your machine
  * AWS free tier eligibility (I claim no responsibility for any credit card charges)
  * A Twilio account with either free tier eligibility or enough credits
  
Assuming you have all these, clone the repo and copy the `config.example.yaml` to `config.yaml` and fill in the values appropriately.
`filesystem_url` is intended to be a valid `s3` bucket url (should be the same defined in your `cloudformation.yaml`), and `atom_feed_url` is the url of the Government of Canada's
weather rss feed for your desired location.

Given AWS resources usually have a globally unique ARN, you'll likely have to change around some of the `cloudformation.yaml` values for
hardcoded constants (e.g `koel-storage` as a `BucketName`).

Once you've done that, run `make deploy`. To tear everything down, run `make destroy`. You may need to `chmod +x` the scripts in the
`/scripts` directory.

## How do I dev on this repository?

Things are set up to make this easy. The `Makefile` provides the common commands for development tasks, like formatting the code
you write or running the tests. `filesystem_url` can also point to a local file for development purposes, which is why the `alerts.json` file has been included
in the repository. `pipenv` was used for package management, so you'll have to run `pipenv install` in order to download the project's dependencies and to ensure the appropriate python version via `make shell`.