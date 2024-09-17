#!/usr/bin/env python
# coding: utf-8

import sys
import pandas as pd
from owlready2 import *

source = str(sys.argv[1])
target = str(sys.argv[2])
language = str(sys.argv[3])

separator = "\t"
mode = "w"

owl = get_ontology(source).load()

classes = list(owl.classes())

obj = {
    "subject_id"            : [],
    "source_language"       : [],
    "translation_language"  : [],
    "source_value"          : [],
    "predicate_id"          : [],
    "translation_value"     : [],
    "translation_status"    : []
}

pd.DataFrame(obj).to_csv(target, sep = separator, header = True, index = False, mode = mode)

mode = "a"

index = 0

for cls in classes:
    index += 1
    print(index)
    name = cls.iri.split("/")[-1]
    obj["subject_id"] = [name]
    
    if hasattr(cls, "label"):
        labels = cls.label
        for label in labels:
            obj["source_language"] = ["en"]
            obj["translation_language"] = ["en"]
            obj["predicate_id"] = ["rdfs:label"]
            obj["source_value"] = [str(label)]
            obj["translation_value"] = [str(label)]
            obj["translation_status"] = ["OFFICIAL"]
            pd.DataFrame(obj).to_csv(target, sep = separator, header = False, index = False, mode = mode)