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

テストケース名を記述したとき(関数のドキュメント)に、空行がないと**D202**のエラーがでたため、除外した.

### テストの導入

標準ライブラリ```unittest```を使用する.
テストレポートを JUnit 形式で出力させるには、```unittest-xml-reporting```を使用する.

```shell
$ pipenv install -d "unittest-xml-reporting~=3.0.3"
```

**unittest_runner.py**にテストの設定(テスト結果の出力先など)を記述する.

カバレッジの計測は```coverage```を導入する.

```shell
$ pipenv install -d coverage~=5.2.1
```

```coverage```の設定は、**.coveragerc**に記述する.



## 参考URL

- [FastAPI](https://fastapi.tiangolo.com/)