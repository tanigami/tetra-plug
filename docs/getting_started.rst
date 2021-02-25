===============
Getting Started
===============

Tetra Plug とは？
---------------

Tetra Plug は、Tetra で動作するコネクションやノートを開発するための Python パッケージです。Tetra 本体の機能やデータにアクセスするためのシンプルなインターフェイスと、必要な部分の開発に集中するためのフレームワークを提供します。また本体と統合せずにローカルで挙動をテストするための仕組みも搭載しています。

Prerequisites
-------------

- Python 3.8+
- Poetry


開発の準備
---------

Cookiecutter のインストール
~~~~~~~~~~~~~~~~~~~~~~~~~
Python パッケージ tetra_plug を単独で利用することも可能ですが、Cookiecutter を使って基本的なプロジェクト構成をつくることができます。

.. code:: shell
    $ pip install cookiecutter

その他のインストール方法については `こちら <https://cookiecutter.readthedocs.io/en/1.7.2/installation.html>`_ を参照してください。

プロジェクトの作成
~~~~~~~~~~~~~~~
.. code:: shell
    $ mkdir xxxx_plug
    $ cd xxxx_plug
    $ cookiecutter https://github.com/tanigami/tetra-plug-boilerplate.git

Next Steps
----------
まずはチュートリアルで基本的な開発のスタイルを学ぶ。
* チュートリアル 1 (Dog API)

