# FastAPIサンプル

## 開発環境

Pipenv + Docker コンテナ


## セットアップ

### pipenvの初期化.

```shell
$ pipenv install --python 3.8
```

### Webフレームワークの導入

```fastapi```のインストール.

```shell
$ pipenv install "fastapi~=0.61.0"
```

```uvicorn```のインストール.

```shell
$ pipenv install "uvicorn~=0.11.8"
```

### Linter の導入

```flake8```と```black```をインストールする.
設定を```.flake8```ファイルに記述する.

importのソートは```isort```を使用する.


以下のコマンドを実行して、インストールする.

```shell
$ pipenv install -d "flake8~=3.8.3"
$ pipenv install -d --pre "black~=19.10b0"
$ pipenv install -d "isort~=5.5.2"
```

black の設定(除外対象など)は`pyproject.toml`に記述する.

`black`でフォーマットしたコードに**E231**の指摘がでるため、除外する.

GitHub Issues #1289 https://github.com/psf/black/issues/1289





### ドキュメント

ドキュメントのスタイルチェックを行う```pydocstyle```と```flake8-docstrings```を使用する.

```shell
$ pipenv install -d "pydocstyle~=5.0.2"
$ pipenv install -d "flake8-docstrings~=1.5.0"
```

### 入力チェック

Emailの検証するためには、```pydantic[email]```がインストールされている必要がある。

```shell
ImportError: email-validator is not installed, run `pip install pydantic[email]`
```

```shell
$ pipenv install "pydantic[email]~=1.6.1"
```

### データベース

非同期処理を実現する.

参考URL: https://fastapi.tiangolo.com/advanced/async-sql-databases/

| 用途 | ライブラリ名 |
| ---- | ---- | 
| モデル定義 | ```SQLAlchemy``` |
| DBアクセス | ```Databases``` |
| マイグレーション管理 | ```Alembic``` |


インストール

```shell
$ pipenv install "SQLAlchemy~=1.3.19"
$ pipenv install "databases~=0.3.2"
$ pipenv install "alembic~=1.4.2"
$ pipenv install "psycopg2~=2.8.5"
$ pipenv install "databases[postgresql]~=0.3.2"
```

alembicの初期化.

```shell
$  alembic init alembic
```

alembic\env.pyを修正する.

DBの接続文字列をiniファイル経由で取得するのではなく、環境変数にある情報をもとに生成する.

デフォルトでは、文字列型の長さが変更した場合に、変更の検出ができないので、以下の記述を追加する.


```python
context.configure(
    # ...
    compare_type = True
)
```

参考URL: [MySQL DB migration: change of string length](https://stackoverflow.com/questions/32536041/mysql-db-migration-change-of-string-length)


#### テーブルの作成方法

以下のコードのように、**declarative_base**を使ってBaseを作成し、そのBaseを継承したモデルを作成すると、Pylanceで継承できないと怒られたため使用しない.


```python
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
```

**MetaData**を使うように変更する.

```
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(16), unique=True),
    Column("email", String(50), unique=True),
)
```

#### コマンド

以下のコマンドを実行して、マイグレーションのファイルを作成する.


```shell
$ alembic revision --autogenerate -m "XXXX"
```


```shell
$ alembic upgrade head
```

### エラーハンドリング

エラーハンドリングは以下のように記述する.

```python
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )
```

main.pyに記述するとコードが肥大化するため、別ファイルに記述する.

```python
def validation_exception_handler(request: Request, exc: RequestValidationError):
    parameters: List[BadRequestParameter] = list()
    for error in exc.errors():
        parameters.append(
            BadRequestParameter(name=error["loc"][1], message=error["msg"])
        )
    error_dto = BadRequestDto(message="入力値が不正です。", parameters=parameters)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(error_dto)
    )

def configure_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
```

main.pyで以下のように記述する.

```python
configure_error_handlers(app)
```
### テスト


### ライブラリのインストール

テストライブラリとして、```pytest```を使用する.
非同期処理のテストには、```pytest-asyncio```を使用する.
HTMLのテストレポートには、```pytest-html```を使用する.
カバレッジの計測には、```pytest-cov```を使用する.

以下のコマンドを実行して、インストールする.

```shell
$ pipenv install -d "pytest~=6.1.0"           # テストライブラリ
$ pipenv install -d "pytest-asyncio~=0.14.0"　# 非同期処理テスト用ライブラリ
$ pipenv install -d "pytest-html~=2.1.1"      # HTMLレポートライブラリ
$ pipenv install -d "pytest-cov~=2.10.1"      # カバレッジ計測
```

設定は、**pyproject.toml**に記述する.

```ini
[tool.pytest.ini_options]
minversion = "6.1"
addopts = '''
  -v
  --junitxml=ci_result/junit.xml
  --cov app
  --cov-report html:ci_result/html-cov
  --cov-report xml:ci_result/cov.xml
'''
testpaths = [
  "tests",
]
```

**addopts**にコマンドパラメータを指定するが、長くなると読みにくいため```'''```を使って記述する.


### HTMLレポートの出力

テスト結果の表にdocstringを表示させる場合、**conftest.py**に自分で処理を記述する必要がある.


```python
from datetime import datetime
from typing import List
from py.xml import Tag, html
import pytest


def pytest_html_results_table_header(cells: List[Tag]):
    cells.insert(1, html.th("Test Case"))
    cells.insert(2, html.th("Time", class_="sortable time", col="time"))
    cells.pop()


def pytest_html_results_table_row(report, cells: List[Tag]) -> None:
    cells.insert(1, html.td(report.description))
    cells.insert(2, html.td(str(datetime.now()), class_="col-time"))
    cells.pop()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)

```


### カバレッジの計測

カバレッジの設定は、**.coveragerc**に記述する.

カバレッジ設定は、以下のサイトを参考にした.

https://pytest-cov.readthedocs.io/en/latest/config.html

カバレッジレポートの出力の設定は、コマンドのパラメータで指定する.






### Visual Studio Codeの設定

#### テストエクスプローラーの設定

```pytest```を実行できるように、**settings.json**を以下のように記述する.

```json
    "pythonTestExplorer.testFramework": "pytest",
    "python.testing.pytestEnabled": true,
    "python.testing.nosetestsEnabled": false,
    "python.testing.unittestEnabled": false,
    "python.testing.pytestPath": ".venv/bin/pytest",
```

#### カバレッジの表示

カバレッジを表示するには、```ryanluker.vscode-coverage-gutters```を使用する.


## 参考URL

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://pypi.org/project/SQLAlchemy/)
- [databases](https://pypi.org/project/databases/)
- [databases document](https://www.encode.io/databases/)
- [alembic](https://pypi.org/project/alembic/)
- [Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/)
- [isort](https://pycqa.github.io/isort/)
- [pytest](https://pypi.org/project/pytest/)
- [pytest 使い方まとめ](https://dev.classmethod.jp/articles/pytest-getting-started/)
- [すぐに使えるpytestによるカバレッジ計測のコマンド](https://qiita.com/kg1/items/e2fc65e4189faf50bfe6)
- [pytest：フィクスチャ(fixture)の使い方](https://qiita.com/_akiyama_/items/9ead227227d669b0564e)
- [pytest ヘビー🐍ユーザーへの第一歩](https://www.m3tech.blog/entry/pytest-summary)
- [pytest-cov’s documentation](https://pytest-cov.readthedocs.io/en/latest/)
- [pytest Configuration](https://docs.pytest.org/en/stable/customize.html)
- [pytest-cov config](https://pytest-cov.readthedocs.io/en/latest/config.html)
- [pytest-html](https://github.com/pytest-dev/pytest-html)