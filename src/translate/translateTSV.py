#!/usr/bin/env python
# coding: utf-8

import sys
import pandas as pd
import translators as ts
import html
import os
import time

sourceFile = str(sys.argv[1])
targetFile = str(sys.argv[2])
sourceLanguage = str(sys.argv[3])
targetLanguage = str(sys.argv[4])
officialFile = str(sys.argv[5])
maxTimeOut = int(sys.argv[6])

translators = ["google", "alibaba", "yandex", "sogou"] # "deepl", "bing",

separator = "\t"
mode = "w"

source = pd.read_csv(sourceFile, sep = separator, na_values='')
official = pd.read_csv(officialFile, sep = separator, na_values='')

count = len(source)

target = pd.DataFrame.from_dict({
    "subject_id"            : source["subject_id"],
    "source_language"       : [sourceLanguage] * count,
    "translation_language"  : [targetLanguage] * count,
    "predicate_id"          : source["predicate_id"],
    "source_value"          : source["source_value"],
    "translation_official"  : [None] * count
})

if os.path.isfile(targetFile):
    target = pd.read_csv(targetFile, sep=separator)
    target.fillna("", inplace = True)

for translator in translators:
    if not translator in target.columns:
        target.insert(len(target.columns), translator, [None] * count)

timeout = 2

for index, row in target.iterrows():

    print("Handling ID {}. ".format(row["subject_id"]), end="")

    translations = list(official["translation_value"][official["subject_id"] == row["subject_id"]])
    if len(translations) == 1:
        target.loc[index, "translation_official"] = translations[0]
    else:
        target.loc[index, "translation_official"] = "ERROR"
        print("No official translation has been found. ", end="")

    success = True

    if row["source_value"]:
        for translator in translators:
            if not target[translator][index] or len(target[translator][index]) == 0:
                try:
                    target.loc[index, translator] = html.unescape(ts.translate_text(query_text = str(row["source_value"]), translator = translator, from_language = sourceLanguage, to_language = targetLanguage))
                except Exception as e:
                    target.loc[index, translator] = ""
                    success = False
                    if (timeout > maxTimeOut):
                        print("Max timeout {} reached. {} has not been translated with {} ({}). ".format(timeout, row["subject_id"], translator, str(e)), end="")
                    else:
                        timeout = timeout * 2
                        print("Timeout set to {}. {} has not been translated with {} ({}). ".format(timeout, row["subject_id"], translator, str(e)), end="")
            else:
                print("Skipping {} with translator {}. ".format(row["subject_id"], translator), end="")
        if success:
            print("Translated successfully.")
        else:
            print("Errors were encountered.")
        time.sleep(timeout)
    else:
        print("No string to translate has been found.")

    target.to_csv(targetFile, sep = separator, index = False, mode = mode)