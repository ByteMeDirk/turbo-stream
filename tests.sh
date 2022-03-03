python -m black .                    # clean up code

python3 -m pipreqs.pipreqs --force . # better version of pip freeze

coverage run -m unittest discover   # run  unittests
coverage report -m && coverage html # produce report
