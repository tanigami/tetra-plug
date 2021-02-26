==========
開発の準備
==========

まず `Cookiecutter <https://cookiecutter.readthedocs.io>`_ を使って、テンプレートからプロジェクトを生成します。


Cookiecutter のインストール
---------------------------

.. code-block:: bash

    $ pip install -U cookiecutter

その他のインストール方法については `こちら <https://cookiecutter.readthedocs.io/en/1.7.2/installation.html>`_ を参照してください。


プロジェクトの作成
------------------

プロジェクトを展開したいディレクトリに移動して、Cookiecutter を実行します。

.. code-block:: bash

    $ cookiecutter https://github.com/tanigami/tetra-plug-boilerplate.git

プロジェクトの生成に必要ないくつかの項目を尋ねられるので、それぞれ入力します。

.. code-block:: bash

    $ cookiecutter https://github.com/tanigami/tetra-plug-boilerplate.git
    package_name [Example Package]: Test Package
    package_slug [test_package]: test_package
    package_short_description []: A test plug package. 
    author_name [Hirofumi Tanigami]: John Doe
    author_email [hirofumi.tanigami@shippinno.co.jp]: johndoe@example.com
    note_name [Go west]: Test Note
    note_slug [test_note]: test_note

入力が完了すると、プロジェクトが生成されます。

.. code-block:: bash

    $ cd tetra_test_package
    $ tree -a -L 4
    .
    ├── .github
    │   └── workflows
    │       └── publish-to-test-pypi.yml
    ├── .gitignore
    ├── Makefile
    ├── README.rst
    ├── pyproject.toml
    └── tetra_test_package
        ├── __init__.py
        ├── connections
        └── notes
            └── test_note
                ├── __init__.py
                ├── echo.py
                ├── play.py
                ├── spec.py
                ├── test.py
                └── tone.py

これでパッケージ開発の準備は完了です。


ここからどうする？
------------------

チュートリアルを参考に単純なノートを実際に作ってみて、開発の流れを把握しましょう。

* チュートリアル 1 (feat. Dog API)