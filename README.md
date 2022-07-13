# Cookiecutter for bali style service

### QuickStart
```shell
pip3 install cookiecutter
cookiecutter https://github.com/bali-framework/cookiecutter-bali.git
cd your_project
mv .env_example .env
git init
make env
```

### Testing
```shell
tox
```

### Service include
* FastAPI
* RocketMQ
* gRPC

#### tip: bali is not design for aio project

### Hooks in pre commit
* pre-commit-hooks
* black
* isort
* flake8

### By default, bali is run at Indonesia, but you can change this in .env file
```dotenv
LOCALE=zh_CN.UTF-8
TZ=Asia/Shanghai
```

### SQLAlchemy field tracking example
```python
from bali.db import AwareDateTime, db
from bali.utils import timezone
from sqlalchemy import BigInteger, Column

from models.field_tracker import FieldTracker


class Example(db.BaseModel):
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    example_time_1 = Column(AwareDateTime, default=timezone.now)
    example_time_2 = Column(AwareDateTime, default=timezone.now)


FieldTracker.listen_for(
    Example.example_time_1,
    Example.example_time_2,
)
```

### MQ consumer example
```python
from loguru import logger
from mq_http_sdk.mq_consumer import Message

from services.mq.base_consumer import BaseConsumer


class Example(BaseConsumer):
    topic = "example"
    group = "example"

    def onmessage(self, msg: Message) -> None:
        logger.info("Hello {}", msg)
```

### MQ producer example
```python
from pydantic import BaseModel

from helpers.base_mq_topic import BaseTopic


class Example(BaseTopic):
    topic = "example"

    class Schema(BaseModel):
        uuid: str
        user_uuid: str
```

### MQ transactional-message example
```python
from pydantic import BaseModel

from helpers.base_mq_topic import TransactionTopic


class ActivationTransaction(TransactionTopic):
    group = "example"
    topic = "transactional-message"
    tag = "example-activation"

    class Schema(BaseModel):
        content: str


with ActivationTransaction(content="wow"):
    pass
```

### Biz example (Biz is used to realize the business)
```python
from biz.model_biz import ModelBiz
from models.example import Example


class ExampleBiz(ModelBiz):
    model = Example
```
