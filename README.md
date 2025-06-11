#### ONLYSANDS

Your guide to all the beaches in Sydney, Australia.

### Useful Commands

`make setup` - build the image and run it locally

`make push` - push the image to docker hub

`make deploy-test` - deploy the image in the test environment

`python manage.py import_beaches /path/to/beaches.csv` - import a csv of beaches

`kubectl exec -it $(kubectl get pods -n onlysands-test -l "app in (django)" -o jsonpath="{.items[0].metadata.name}") -n onlysands-test -- /bin/bash` - ssh into test django container
