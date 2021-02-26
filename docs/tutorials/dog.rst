================================
チュートリアル 1 (feat. Dog API)
================================

`Dog API <https://dog.ceo/dog-api/>`_ は、犬の画像の URL を取得するための API です。
この API を Tetra から利用するためのノートを作ってみましょう。

このチュートリアルを通して、以下のことが学べます。

* ノート実装の基本
* ノートのテストの基本


どんなノート？
--------------

これから作るノートの仕様を整理します。

Dog API には画像の取得方法ごとにいくつかのエンドポイントがありますが、今回はその中から「犬種を指定してランダムな画像を取得する」エンドポイントを利用しましょう。トーンには「犬種」をドロップダウンメニューで設定でき、エコーは取得した画像の URL があればよさそうです。

また「犬種」が設定されていない状態では実行できないので、トーンフィールドにエラーも表示する必要があります。


プロジェクトの作成
------------------

.. code-block:: bash

    $ cookiecutter https://github.com/tanigami/tetra-plug-boilerplate.git
    package_name [Example Package]: Dog
    package_slug [dog]: dog
    package_short_description []: A dog plug package. 
    author_name [Hirofumi Tanigami]: John Doe
    author_email [hirofumi.tanigami@shippinno.co.jp]: johndoe@example.com
    note_name [Go west]: 犬のランダム画像を取得する
    note_slug [test_note]: get_random_dog_image

    $ cd tetra_dog
    $ poetry update


トーンの定義
------------

どこから始めてもよいですが、今回はトーンの定義からやっていきます。
生成された `get_random_dog_image` モジュールの `tone.py` に空っぽの関数がひとつあります。

.. code-block:: python

    def tone(tetra: Supply) -> Sequence:
        return []

この `tone` 関数がトーンの定義を返すようにします。「犬種」をドロップダウンメニューで選べる必要がありました。

.. code-block:: python

    def tone(tetra: Supply) -> Sequence:
        return [
            {
                "key": "breed",
                "type": "select",
                "label": "犬種",
                "options": lambda tetra: {
                    "shiba": "柴",
                    "pug": "パグ",
                    "mix": "ミックス",
                },
                "validators": [required.validate()],
            },
        ]

こんな感じです。。トーンのキーは `breed` です。


エコーの定義
------------

次に、`echo.py` にエコーの定義を書いてみましょう。「画像 URL」を文字列型で扱うエコーをひとつ設定します。

.. code-block:: python

    def echo(tetra: Supply) -> Mapping:
        return {
            "image": {
                "name": "画像 URL",
                "type": "string",
            }
        }

よさそうです。エコーのキーは `image` としました。


実行処理の実装
--------------

いよいよ、`play.py` で実行処理の実装に入ります。

さきほど定義した `breed` フィールドの入力値を使って Dog API をたたき、返ってきた画像 URL を `image` エコーとして残します。
`play()` 関数に引数として渡される `tetra` のメソッド `get_input()` と `leave_echo()` を使います。
エラーが発生した場合は `halt()` メソッドで実行を中止します。

.. code-block:: python

    def play(tetra: Supply) -> None:
        breed = tetra.get_input(field_key="breed")

        image, error = _get_random_image(breed=breed, tetra=tetra)

        if error is not None:
            tetra.halt(
                message=f"エラーが発生しました - {error}"
            )

        tetra.log(
            level="INFO",
            message=f"{breed} の画像を取得しました。"
        )

        tetra.leave_echo("image", image)


    def _get_random_image(breed: str, tetra: Supply) -> Tuple[Optional[str], Any]:
        try:
            if tetra.testing:
                response = tetra.testing["response"](breed=breed)
            else:
                response = requests.get(
                    f"https://dog.ceo/api/breed/{breed}/images/random"
                ).json()
        except Exception as e:
            return None, str(e)

        if response["status"] == "success":
            return response["message"], None
        else:
            return None, response["message"]

エラーのことも考えると少し複雑になります。

実行に必要な実装は以上ですが、テストもしましょう。


テストをする
------------

これまでの実装をテストしますが、`tetra_plug` パッケージにはテストのフレームワークも用意されているので、開発者としてやるべきは `spec.py` での仕様の記述だけです。
`tone` にはトーンの入力値のパターンとそれに対応して期待されるフィールドエラーの状態を、`play` にはトーンの入力値と、実行して残るはずのエコーやログを記述します。

.. code-block:: python

    tone = [
        {
            "__desctiption__": "デフォルトの状態",
            "tone": {},
            "state": {"breed": {"input": None, "errors": []}},
        },
        {
            "__desctiption__": "breed が未選択である",
            "tone": {"breed": ""},
            "state": {"breed": {"input": "", "errors": [required.message()]}},
        },
        {
            "__desctiption__": "breed に不正な値がある",
            "tone": {"breed": "cat"},
            "state": {"breed": {"input": "cat", "errors": [options.message()]}},
        },
        {
            "__desctiption__": "すべて正しく設定されている",
            "tone": {"breed": "shiba"},
            "state": {"breed": {"input": "shiba", "errors": []}},
        },
    ]

.. code-block:: Python

    def raise_error(message):
        raise Exception(message)

    play = [
        {
            "__desctiption__": "OK のとき",
            "tone": {"breed": "shiba"},
            "testing": {
                "response": lambda breed: {
                    "message": f"https://images.dog.ceo/breeds/{breed}/{breed}-1.jpg",
                    "status": "success",
                }
            },
            "logs": [
                {
                    "level": "INFO",
                    "message": "shiba の画像を取得しました。",
                    "context": None,
                }
            ],
            "echo": {"image": "https://images.dog.ceo/breeds/shiba/shiba-1.jpg"},
        },
        {
            "__desctiption__": "API エラーのとき",
            "tone": {"breed": "cat"},
            "testing": {
                "response": lambda breed: {
                    "status": "error",
                    "message": "Breed not found (master breed does not exist)",
                    "code": 404,
                }
            },
            "logs": [
                {
                    "level": "ERROR",
                    "message": "エラーが発生しました - Breed not found (master breed does not exist)"
                }
            ],
            "echo": {},
            "halted": True,
        },
        {
            "__desctiption__": "例外のとき",
            "tone": {"breed": "cat"},
            "testing": {
                "response": lambda breed: raise_error("Something's just happened!")
            },
            "logs": [
                {
                    "level": "ERROR",
                    "message": "エラーが発生しました - Something's just happened!"
                }
            ],
            "echo": {},
            "halted": True,
        },
    ]

仕様の記述が終わったら、テストを実行します。

.. code-block:: bash

    $ make test
    pytest
    .......                                                            [100%]
    7 passed in 0.18s

おめでとうございました。