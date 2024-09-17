#!/usr/bin/env python
# coding: utf-8

import translators as ts

translators = ["google", "alibaba", "yandex", "sogou"] #["google", "deepl", "alibaba", "bing", "argos", "caiyun", "yandex", "sogou"]
test = "This is a test sentence."

for translator in translators:
    try:
        ts.translate_text(query_text = test, translator = translator, from_language = "en", to_language = "fr")
        print("{} was successful.".format(translator))
    except Exception as e:
        print("{} was not successful: ".format(translator), end="")
        print(e)

print("Test finished.")
    