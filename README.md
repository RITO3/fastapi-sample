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

以下のコマンドを実行して、インストールする.

```shell
$ pipenv install -d "flake8~=3.8.3"
$ pipenv install -d --pre "black~=19.10b0"
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


### テーブルの作成方法

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

## 参考URL

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://pypi.org/project/SQLAlchemy/)
- [databases](https://pypi.org/project/databases/)
- [alembic](https://pypi.org/project/alembic/)