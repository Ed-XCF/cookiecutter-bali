env:
	rm -rf venv
	python3 -m venv venv
	. venv/bin/activate \
	&& python3 -m pip install --upgrade pip \
	&& pip3 install wheel pre-commit git+https://github.com/Ed-XCF/bali-cli.git@v0.5.14#egg=bali-cli \
	&& pip3 install -r requirements_dev.txt \
	&& pre-commit install

docker:
	pip3 install wheel pre-commit git+https://github.com/Ed-XCF/bali-cli.git@v0.5.14#egg=bali-cli
	pre-commit install
	docker build --rm --build-arg DEPS=requirements_dev . -t {{cookiecutter.repo_name}}

migration:
	alembic revision --autogenerate

migrate:
	alembic upgrade head

clean-git:
	git branch --merged | egrep -v "master|main|test|dev|develop" | xargs git branch -d
	git fetch -p origin && git branch -r --merged | egrep -v "master|main|test|dev|develop" | sed 's/origin\///' | xargs git push origin -d
