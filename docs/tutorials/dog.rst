Dog API
=======

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


Tone
----

.. code-block:: python

    from typing import Sequence
    from tetra_plug import Supply
    from tetra_plug.validators import required

    def tone(tetra: Supply) -> Sequence:
            """Retrieve all the items."""
        return [
        
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

Echo
----

.. code-block:: python

    from typing import Mapping
    from tetra_plug import Supply

    def echo(tetra: Supply) -> Mapping:
            """Retrieve all the items."""
        return {
            
        }

ffff

.. code-block:: python

    return {
        "image": {
            "name": {"ja": "画像 URL", "en": "Image URL"},
            "type": "string",
        }
    }

Play
----

.. code-block:: python

    from tetra_plug import Supply

    def play(tetra: Supply) -> None:
        pass
    ```

`[play.py](http://play.py)` に `play()` 関数がつくられてます。ここにノートが行う処理を実装します。

`Supply` 型の引数 `tetra` から、Tetra の機能や値にアクセスできます。
`get_input()` `log()` `halt()`  

.. code-block:: python

    def play(tetra: Supply) -> None:
        """Retrieve all the items."""
        breed = tetra.get_input(field_key="breed")

            try:
                    response = requests.get(f"https://dog.ceo/api/breed/{breed}/images/random")
            except:
                    tetra.halt(
                            message={
                                    "ja": "エラー",
                                    "en": "Error",
                            }
                    )

        tetra.log(
                    level="DEBUG",
                    message={
                        "ja": "OK",
                        "en": "OK",
                    }
            )

            tetra.echo("image", response.json()["message"])

Spec
----

.. code-block:: python
    {
        ...
    }

Test
----
