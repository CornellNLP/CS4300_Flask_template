import math
import json
import os
import random
import requests
import datacommons as dc
import datacommons_pandas as dcp


def handle55To64(dcid):
    x1 = dc.get_stat_value(dcid, "Count_Person_55To59Years")
    x2 = dc.get_stat_value(dcid, "Count_Person_60To61Years")
    x3 = dc.get_stat_value(dcid, "Count_Person_62To64Years")
    return x1+x2+x3


class Handler:
    def __init__(self):
        self.not_supported_fields = {"Count_Person_55To64Years": handle55To64}
        self.not_supported_city_fields = {
            # ("geoId/3712000", "Count_CriminalActivities_CombinedCrime"): handleCharlotteCrime
        }

    def not_supported(self, dcid, fieldName):
        b1 = fieldName in self.not_supported_fields
        b2 = (dcid, fieldName) in self.not_supported_city_fields
        if b1:
            return (b1, self.not_supported_fields[fieldName])
        elif b2:
            return (b2, self.not_supported_city_fields[(dcid, fieldName)])
        else:
            return (False, None)

    def handle55To64(self, dcid):
        x1 = dc.get_stat_value(dcid, "Count_Person_55To59Years")
        x2 = dc.get_stat_value(dcid, "Count_Person_60To61Years")
        x3 = dc.get_stat_value(dcid, "Count_Person_62To64Years")
        return x1+x2+x3


class DatasetBuilder:
    def __init__(self):
        self.dataset = {}
        self.handler = Handler()
        self.dcid_to_city_name = {}
        self.category_name_to_field_name = {}

    def __addNameCol(self, df):
        df['name'] = df.index.map(dc.get_property_values(df.index, 'name'))
        df['name'] = df['name'].str[0]

    def writeDatasetToJsonFile(self, outfile):
        with open(outfile, "w") as f:
            json.dump(self.dataset, f)
            print("\n\nWrote data to", outfile)
        return

    def __getDcidsToNameForTopNCities(self, n=100):
        allcities = dcp.get_places_in(["country/USA"], "City")["country/USA"]
        df = dcp.build_multivariate_dataframe(allcities, ["Count_Person"])
        self.__addNameCol(df)
        df = df.sort_values("Count_Person", ascending=False)[:100]
        return df["name"].to_dict()

    def __loadSchema(self, schema_file="schema.json"):
        print("loading schema")
        with open(schema_file, "r") as f:
            schema = json.load(f)
            self.category_name_to_field_name = schema["category_name_to_field_name"]
        try:
            # see if schema has dcid_to_city_name
            # if not, get it and add it, then reload schema
            self.dcid_to_city_name = schema["dcid_to_city_name"]
            print("found dcid to city name")
        except KeyError:
            print("got key error")
            with open(schema_file, "w") as f:
                schema = {}
                dcidToName = self.__getDcidsToNameForTopNCities()
                print(dcidToName)
                schema["dcid_to_city_name"] = dcidToName
                schema["category_name_to_field_name"] = self.category_name_to_field_name
                json.dump(schema, f)
            self.__loadSchema(schema_file)
        return

    def __buildJsonDataFromSchema(self, dcid_to_city_name=None, category_name_to_field_name=None, outfile="dataset.json", verbose=False):
        if dcid_to_city_name is None:
            if self.dcid_to_city_name == {}:
                self.__loadSchema()
            dcids = self.dcid_to_city_name
        else:
            dcids = dcid_to_city_name

        if category_name_to_field_name is None:
            if self.category_name_to_field_name == {}:
                self.__loadSchema()
            category_names = self.category_name_to_field_name
        else:
            category_names = category_name_to_field_name

        for dcid, city_name in dcids.items():
            self.dataset[dcid] = {}
            self.dataset[dcid]["city_name"] = city_name
            if verbose:
                print("##############   ", city_name,
                      "   ##############", "\n\n")
            for cat_name, stat_name in category_names.items():
                # if stat_name in self.handler.not_supported:
                ns = self.handler.not_supported(dcid, stat_name)
                if ns[0]:
                    f = ns[1]
                    x = f(dcid)
                else:
                    x = dc.get_stat_value(dcid, stat_name)
                if verbose:
                    print(cat_name, ":", x)
                if math.isnan(x):
                    print("***Got NaN for", city_name, ",", cat_name)
                self.dataset[dcid][cat_name] = x

            print("Finished data collection for", city_name)
        self.writeDatasetToJsonFile(outfile)
        return

    def buildSampleDataset(self, sample_file="sample.json"):
        with open("sample.json", "r") as f:
            schema = json.load(f)
            self.__buildJsonDataFromSchema(
                schema["dcid_to_city_name"], schema["category_name_to_field_name"], outfile="dataset_sample.json")

    def buildFullDataset(self):
        self.__buildJsonDataFromSchema()


dsb = DatasetBuilder()
dsb.buildSampleDataset()
