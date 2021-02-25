Dog API を Plug
==============

つくるもの
-----

Dog API からある犬種のランダム画像の URL を取得するノート。ノートだけ。コネクションなし。




ノートの作成
------
.. code-block:: 

    $ cd notes
    $ cookiecutter https://github.com/shippinno/tetra_plug.git --directory=note
    $ cd get_breed_random
    $ tree -a -L 1
    .
    ├── echo.py
    ├── play.py
    ├── spec.py
    ├── tone.py
    └── __init


トーンの定義
------

.. code-block:: python

    def tone(tetra: Supply) -> Sequence:
        return [
            {
                "key": "breed",
                "type": "select",
                "label": {"ja": "犬種", "en": "Breed"},
                "options": lambda tetra: {
                    "shiba": {"ja": "柴", "en": "Shiba"},
                    "pug": {"ja": "パグ", "en": "Pug"},
                    "mix": {"ja": "ミックス", "en": "Mix"},
                },
                "validators": [required.validate()],
            },
        ]

sss

.. code-block:: python

    return [
            {
            "key": "breed",
            "type": "select",
            "label": {"ja": "犬種", "en": "Breed"},
            "options": { ... },
            "validators": [required],
        },
    ]


エコーの定義
------

.. code-block:: python

    def echo(tetra: Supply) -> Mapping:
        return {
            "image": {
                "name": {"ja": "画像 URL", "en": "Image URL"},
                "type": "string",
            }
        }


ffff

.. code-block:: python

    return {
        "image": {
            "name": {"ja": "画像 URL", "en": "Image URL"},
            "type": "string",
        }
    }


実行処理の実装
-------

.. code-block:: python

    def play(tetra: Supply) -> None:
        pass
  

`[play.py](http://play.py)` に `play()` 関数がつくられてます。ここにノートが行う処理を実装します。

`Supply` 型の引数 `tetra` から、Tetra の機能や値にアクセスできます。
`get_input()` `log()` `halt()`  

.. code-block:: python

    def play(tetra: Supply) -> None:
        breed = tetra.get_input(field_key="breed")

        image, error = _get_random_image(breed=breed, tetra=tetra)

        if error is not None:
            tetra.halt(
                message={
                    "ja": f"エラーが発生しました - {error}",
                    "en": f"Error - {error}",
                }
            )

        tetra.log(
            level="INFO",
            message={
                "ja": f"{breed} の画像を取得しました。",
                "en": f"Found {breed} image.",
            },
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


テスト
----

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
                    "message": {"ja": "shiba の画像を取得しました。", "en": "Found shiba image."},
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
                    "message": {
                        "ja": "エラーが発生しました - Breed not found (master breed does not exist)",
                        "en": "Error - Breed not found (master breed does not exist)",
                    },
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
                    "message": {
                        "ja": "エラーが発生しました - Something's just happened!",
                        "en": "Error - Something's just happened!",
                    },
                }
            ],
            "echo": {},
            "halted": True,
        },
    ]

