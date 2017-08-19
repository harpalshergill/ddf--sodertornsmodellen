
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import os
from ddf_utils.str import to_concept_id
#from ddf_utils.index import create_index_file


# ## Files & Dirs

# In[39]:

# Directories
out_dir = os.path.join(os.pardir, os.pardir, "ddf--sodertornsmodellen--src")
src = os.path.join(os.pardir, "source")

# Raw data
entities_file_1 = os.path.join(src, "161115 A7 utan formler.xlsx") # Basomrande from Statistics Sweden
entities_file_2 = os.path.join(src, "kommunlankod.xls") # Municipalities from Statistics Sweden
datapoints_file = os.path.join(src, "Basområdesdata hela länet.xlsx") # Municipality data


# ## Translation dict for column names

# In[40]:

column_names = {    
    "År": "year",
    "Kommun": "geo",
    "Basområde": "basomrade",
    # Education sheet
    "Förgymnasial, Män": "educational_level_pre_secondary_school_aged_25_64_male",
    "Förgymnasial, Kvinnor": "educational_level_pre_secondary_school_aged_25_64_female",
    "Gymnasial, Män": "educational_level_secondary_school_aged_25_64_male",
    "Gymnasial, Kvinnor": "educational_level_secondary_school_aged_25_64_female",
    "EfterGymnasial <= 3 år, Män": "educational_level_higher_education_max_3_years_aged_25_64_male",
    "EfterGymnasial <= 3 år, Kvinnor": "educational_level_higher_education_max_3_years_aged_25_64_female",
    "EfterGymnasial > 3 år, Män": "educational_level_higher_education_min_3_years_aged_25_64_male",
    "EfterGymnasial > 3 år, Kvinnor": "educational_level_higher_education_min_3_years_aged_25_64_female",
    "Uppgift saknas, Män": "missing_data_male",
    "Uppgift saknas, Kvinnor": "missing_data_female",
    "Totalt antal personer 25-64 år, Män": "population_aged_25_64_male",
    "Totalt antal personer 25-64 år, Kvinnor": "population_aged_25_64_female",
    "Totalt antal personer 25-64 år, Totalt": "population_aged_25_64",
    # Employment sheet
    "Antal förvärvsarbetande, Män": "employed_aged_20_64_male",
    "Antal förvärvsarbetande, Kvinnor": "employed_aged_20_64_female",
    "Antal ej förvärvsarbetande, Män": "unemployed_aged_20_64_male",
    "Antal ej förvärvsarbetande, Kvinnor": "unemployed_aged_20_64_female",
    "Totalt antal personer 20-64 år, Män": "population_aged_20_64_male",
    "Totalt antal personer 20-64 år, Kvinnor": "population_aged_20_64_female",
    "Totalt antal personer 20-64 år, Totalt": "population_aged_20_64",
    # Income sheet
    "Låg inkomst, Män": "low_income_aged_lt_20_male",
    "Låg inkomst, Kvinnor": "low_income_aged_lt_20_female",
    "Medellåg inkomst, Män": "lower_middle_income_aged_lt_20_male",
    "Medellåg inkomst, Kvinnor": "lower_middle_income_aged_lt_20_female",
    "Medelhög inkomst, Män": "upper_middle_income_aged_lt_20_male",
    "Medelhög inkomst, Kvinnor": "upper_middle_income_aged_lt_20_female",
    "Hög inkomst, Män": "high_income_aged_lt_20_male",
    "Hög inkomst, Kvinnor": "high_income_aged_lt_20_female",
    "Totalt antal personer 20+ år, Män": "population_aged_lt_20_male",
    "Totalt antal personer 20+ år, Kvinnor": "population_aged_lt_20_female",
    "Totalt antal personer 20+ år, Totalt": "population_aged_lt_20",
    "Medianinkomst, Män": "median_income_aged_lt_20_male",
    "Medianinkomst, Kvinnor": "median_income_aged_lt_20_female",
    "Medianinkomst, Totalt": "median_income_aged_lt_20",
    "Medelinkomst, Män": "mean_income_aged_lt_20_male",
    "Medelinkomst, Kvinnor": "mean_income_aged_lt_20_female",
    "Medelinkomst, Totalt": "mean_income_aged_lt_20",
    "Summa inkomst, Män": "sum_income_aged_lt_20_male",
    "Summa inkomst, Kvinnor": "sum_income_aged_lt_20_female",
    "Summa inkomst, Totalt": "sum_income_aged_lt_20",
    # Work sheets
    # 1
    "Antal, Inflyttade, Män": "immigration_male",
    "Antal, Inflyttade, Kvinnor": "immigration_female",
    "Antal, Utflyttade, Män": "emigration_male",
    "Antal, Utflyttade, Kvinnor": "emigration_female",
    "Antal, Befolkning 20XX-12-31, Män": "population_20xx_12_31_male",
    "Antal, Befolkning 20XX-12-31, Kvinnor": "population_20xx_12_31_female",
    "Andelar, Inflyttade, Män": "share_immigration_male",
    "Andelar, Inflyttade, Kvinnor": "share_immigration_female",
    "Andelar, Inflyttade, Totalt": "share_immigration",
    "Andelar, Utflyttade, Män": "share_emigration_male",
    "Andelar, Utflyttade, Kvinnor": "share_emigration_female",
    "Andelar, Utflyttade, Totalt": "share_emigration",
    # 2
    "Antal, Inflyttade 20-64 år \nsom förvärvsarbetar, Män": "immigration_employed_aged_20_64_male",
    "Antal, Inflyttade 20-64 år \nsom förvärvsarbetar, Kvinnor": "immigration_employed_aged_20_64_female",
    "Antal, Utflyttade 20-64 år \nsom förvärvsarbetar, Män": "emigration_employed_aged_20_64_male",
    "Antal, Utflyttade 20-64 år \nsom förvärvsarbetar, Kvinnor": "emigration_employed_aged_20_64_female",
    "Antal, Befolkning 20-64 år 2000-12-31 som förvärvsarbetar, Män": "population_20xx_12_31_employed_aged_20_64_male",
    "Antal, Befolkning 20-64 år 2000-12-31 som förvärvsarbetar, Kvinnor": "population_20xx_12_31_employed_aged_20_64_female",
    "Andelar, Inflyttade 20-64 år \nsom förvärvsarbetar, Män": "share_immigration_employed_aged_20_64_male",
    "Andelar, Inflyttade 20-64 år \nsom förvärvsarbetar, Kvinnor": "share_immigration_employed_aged_20_64_female",
    "Andelar, Inflyttade 20-64 år \nsom förvärvsarbetar, Totalt": "share_immigration_employed_aged_20_64",
    "Andelar, Utflyttade 20-64 år \nsom förvärvsarbetar, Män": "share_emigration_employed_aged_20_64_male",
    "Andelar, Utflyttade 20-64 år \nsom förvärvsarbetar, Kvinnor": "share_emigration_employed_aged_20_64_female",
    "Andelar, Utflyttade 20-64 år \nsom förvärvsarbetar, Totalt": "share_emigration_employed_aged_20_64",
    # 3
    "Antal, Inflyttade 25-64 år som har minst 3-årig högskoleutbildning, Män": \
    "immigration_min_3_years_of_higher_education_aged_25_64_male",
    "Antal, Inflyttade 25-64 år som har minst 3-årig högskoleutbildning, Kvinnor": \
    "immigration_min_3_years_of_higher_education_aged_25_64_female",
    "Antal, Utflyttade 25-64 år som har minst 3-årig högskoleutbildning, Män": \
    "emigration_min_3_years_of_higher_education_aged_25_64_male",
    "Antal, Utflyttade 25-64 år som har minst 3-årig högskoleutbildning, Kvinnor": \
    "emigration_min_3_years_of_higher_education_aged_25_64_female",
    "Antal, Befolkning 25-64 år, 2000-12-31 som har minst 3-årig högskoleutbildning 25-64 år, Män": \
    "population_25xx_12_31_min_3_years_of_higher_education_aged_25_64_male",
    "Antal, Befolkning 25-64 år, 2000-12-31 som har minst 3-årig högskoleutbildning 25-64 år, Kvinnor": \
    "population_25xx_12_31_min_3_years_of_higher_education_aged_25_64_female",
    "Andelar, Inflyttade 25-64 år som har minst 3-årig högskoleutbildning, Män": \
    "share_immigration_min_3_years_of_higher_education_aged_25_64_male",
    "Andelar, Inflyttade 25-64 år som har minst 3-årig högskoleutbildning, Kvinnor": \
    "share_immigration_min_3_years_of_higher_education_aged_25_64_female",
    "Andelar, Inflyttade 25-64 år som har minst 3-årig högskoleutbildning, Totalt": \
    "share_immigration_min_3_years_of_higher_education_aged_25_64",
    "Andelar, Utflyttade 25-64 år som har minst 3-årig högskoleutbildning, Män": \
    "share_emigration_min_3_years_of_higher_education_aged_25_64_male",
    "Andelar, Utflyttade 25-64 år som har minst 3-årig högskoleutbildning, Kvinnor": \
    "share_emigration_min_3_years_of_higher_education_aged_25_64_female",
    "Andelar, Utflyttade 25-64 år som har minst 3-årig högskoleutbildning, Totalt": \
    "share_emigration_min_3_years_of_higher_education_aged_25_64"
}


# ## Excel sheets' config

# In[41]:

sheet_config = [
    {
        "sheetname": 0,
        "skiprows": [0,1,2],
        "parse_cols": "A:P",
        "no_headers": 2,
        "name": "education"
    },
    {
        "sheetname": 1,
        "skiprows": [0,1,2],
        "parse_cols": "A:J",
        "no_headers": 2,
        "name": "employment"
    },
    {
        "sheetname": 2,
        "skiprows": [0,1,2,4,5,6],
        "parse_cols": "A:W",
        "no_headers": 2,
        "name": "income"
    },
    {
        "sheetname": 3,
        "skiprows": [0,1,2,4,5,6],
        "parse_cols": "A:O",
        "no_headers": 3,
        "name": "total migration"
    },
    {
        "sheetname": 4,
        "skiprows": [0,1,2,4,5,6],
        "parse_cols": "A:O",
        "no_headers": 3,
        "name": "migration employment"
    },
    {
        "sheetname": 5,
        "skiprows": [0,1,2,4,5,6],
        "parse_cols": "A:O",
        "no_headers": 3,
        "name": "migration education"
    }
]


# ## Helpers

# In[42]:

def map_to_id(x):
    if x == str("Stockholms län"):
        return to_concept_id("01 " + x)
    elif x == "Riket":
        return to_concept_id("swe")
    else:
        return to_concept_id(x)


# In[43]:

def generate_code_dict(df):
    
    code_to_id = df.copy()
    code_to_id["code"] = code_to_id["basomrade"].apply(lambda x: str(x).split("_")[0])
    code_to_id = code_to_id[["code", "basomrade"]]
    code_to_id = code_to_id.set_index("code")
    code_to_id = code_to_id.to_dict()["basomrade"]
    
    return code_to_id


# ## Process data

# In[44]:

def process_data(data, b_names, column_names, no_headers, sheetname):

    data = data.copy()
    
    # Join header rows
    for i in range(0, no_headers-1):
        data.iloc[i] = data.iloc[i].fillna(method="ffill")
        data.iloc[i] = data.iloc[i].fillna("")
        
    for i in range(0, no_headers-1):
        data.iloc[i+1] = data.iloc[i:i+2].apply(lambda x: ', '.join([y.strip() for y in x if y]), axis=0)
    data.columns = data.iloc[no_headers-1]
    
    data = data.iloc[no_headers-1:]

    # Remove non real rows
    data = data[data[data.columns[0]].apply(np.isreal)] 

    # Encode in utf-8 to enable renaming
    #data.columns = data.columns.map(lambda x: str(x).encode("utf-8"))
    #column_names = {k: str(v).encode("utf-8") for k,v in column_names.items()}
    column_names = {k: v for k,v in column_names.items()}

    # Rename columns
    data = data.rename(columns = column_names)
    
    # Remove "Totalt"
    data["basomrade"] = data["basomrade"].apply(lambda x: str(x) if x != "Totalt" else "")
    
    # Transform names into IDs
    data["geo"] = data["geo"].apply(map_to_id)
    
    # Drop Vaxholm 43
    if sheetname in [3,4,5]:
        data = data.drop(data[(data["geo"] == "0187_vaxholm") & (data["basomrade"] == "3411130")].index)
    
    return data


# ## Entities

# In[45]:

def extract_entities_basomraden(data, names):

    basomraden = data.copy()
    names = names.copy()
    
    # Rename columns
    basomraden = basomraden[basomraden["basomrade"] != ""]
    basomraden = basomraden[["basomrade", "geo"]]
    basomraden.rename(columns={"geo": "municipality"}, inplace=True)
    basomraden.drop_duplicates("basomrade", inplace=True)
    names.rename(columns={2010: "basomrade", "namn": "name"}, inplace=True)
    
    # Merge to get name
    basomraden = basomraden.merge(names, how="left", on="basomrade")
    
    # Concatenate code and name as ID
    basomraden["name"] = basomraden["name"].apply(lambda x: "" if pd.isnull(x) else x)
    basomraden["basomrade"] = basomraden["basomrade"].map(str) + " " + basomraden["name"]
    basomraden["name"] = basomraden[["basomrade", "name"]].apply(lambda x: str(x[0]) if x[1] == "" else x[1], axis=1)
    basomraden["basomrade"] = basomraden["basomrade"].map(to_concept_id)
    basomraden["is--basomrade"] = "TRUE"
    
    return basomraden[["basomrade", "name", "municipality", "is--basomrade"]]


# In[46]:

def extract_entities_municipalities(data):

    muni = data.copy()
    muni.rename(columns = {"Code": "municipality", "Name": "name"}, inplace=True)
    muni = muni[muni["municipality"].str.startswith("01")] # Select only municipalities in Stockholm county
    muni = muni.ix[1:] # Remove county row
    muni["county"] = "01_stockholms_l_n"
    muni["is--municipality"] = "TRUE"
    muni["municipality"] = muni["municipality"] + " " + muni["name"]
    muni["municipality"] = muni["municipality"].map(to_concept_id)
    
    return muni


# In[47]:

def extract_entities_counties(data):
    
    counties = data.copy()
    counties.rename(columns = {"Code": "county", "Name": "name"}, inplace=True)
    counties = counties[counties["county"] == '01'] # Select Stockholm county
    counties["county"] = counties["county"] + " " + counties["name"]
    counties["county"] = counties["county"].map(to_concept_id)
    counties["country"] = "swe"
    counties["is--county"] = "TRUE"
    
    return counties


# In[48]:

def extract_entities_county_region():
    
    county_regions = pd.DataFrame(data =                         {"county_region": ["s_dert_rn"],                          "name": ["Södertörn"],                          "county": ["01_stockholms_l_n"],                          "is--county_region": ["TRUE"]},                         columns=["county_region", "name", "county", "is--county_region"])
    
    return county_regions


# In[49]:

def extract_entities_countries():
    
    countries = pd.DataFrame(data = {"country": ["swe"], "name": ["Riket"]}, columns=["country", "name"])
    countries["is--country"] = "TRUE"
    
    return countries


# ## Datapoints

# In[50]:

def extract_datapoints(data, basomraden, municipalities, counties, county_regions, countries):
    
    right = data.copy()
    
    # Join with corresponding entity
    dps_basomraden =     basomraden["basomrade"].to_frame().merge(right, on="basomrade", how="left")
    dps_municipalities =     municipalities["municipality"].to_frame().merge(right[right["basomrade"] == ""],                          left_on="municipality", right_on="geo", how="inner")
    dps_counties =     counties["county"].to_frame().merge(right, left_on="county", right_on="geo", how="inner")
    dps_county_regions =     county_regions["county_region"].to_frame().merge(right, left_on="county_region", right_on="geo", how="inner")
    dps_countries =     countries["country"].to_frame().merge(right, left_on="country", right_on="geo", how="inner")

    return dps_basomraden[[col for col in dps_basomraden.columns if col not in ["geo"]]],     dps_municipalities[[col for col in dps_municipalities.columns if col not in ["geo", "basomrade"]]],    dps_counties[[col for col in dps_counties.columns if col not in ["geo", "basomrade"]]],    dps_county_regions[[col for col in dps_county_regions.columns if col not in ["geo", "basomrade"]]],    dps_countries[[col for col in dps_countries.columns if col not in ["geo", "basomrade"]]]

# ## Concepts

# In[51]:

def extract_concepts(measures, column_names):
    
    concept_file = os.path.join(out_dir, "ddf--concepts.csv")
    
    if (not os.path.isfile(concept_file)):
        #Add some non-measure concepts manually
        manual_data = {"concept":                        ["geo", "domain", "name", "year",                         "basomrade", "municipality", "county", "county_region","country"],                       "concept_type":                        ["entity_domain", "string", "string", "time",                         "entity_set","entity_set", "entity_set", "entity_set", "entity_set"],                       "domain":                        ["", "", "", "",                         "geo", "geo", "geo", "geo", "geo"],                       "name":                        ["Geo", "Domain", "Name", "År",                         "Basområde", "Kommun", "Län", "Länsregion", "Land"]}
        data = pd.DataFrame(data=manual_data, columns=["concept", "name", "concept_type", "domain"])
    else:
        data = pd.read_csv(concept_file, encoding="utf-8")
      
    # Add measures
    inv_col_names = {v: k for k, v in column_names.items()}
    tmp = pd.DataFrame(columns=["concept", "name", "concept_type", "domain"])
    tmp["concept"] = measures
    tmp["concept_type"] = "measure"
    tmp["domain"] = ""
    tmp["name"] = measures.map(lambda x: inv_col_names[x])
    
    data = pd.concat([data, tmp])
    
    return data


# ## Main

# In[52]:

if __name__ == "__main__":
    
    first_run = True
    
    for config in sheet_config:
        
        # READ DATA
        if (first_run):
            b_names = pd.read_excel(entities_file_1, skiprows=[0,1,2,3,4,5,6], converters={2010: lambda x: str(x)})
        if (not first_run): 
            del data
        data = pd.read_excel(datapoints_file, sheetname=config["sheetname"],                              skiprows=config["skiprows"], parse_cols=config["parse_cols"])
        # PROCESS DATA
        data = process_data(data, b_names, column_names, config["no_headers"], config["sheetname"])

        # ENTITIES
        if (first_run):
            print (" ------ Entities ------ ")
            e_data = pd.read_excel(entities_file_2, skiprows=[0,1,2,3,4], converters={'Code': lambda x: str(x)})

            df_basomraden = extract_entities_basomraden(data, b_names)
            df_municipalities = extract_entities_municipalities(e_data)
            df_counties = extract_entities_counties(e_data)
            df_county_regions = extract_entities_county_region()
            df_countries = extract_entities_countries()

            entities = [df_basomraden, df_municipalities, df_counties, df_county_regions, df_countries]
            entity_name = ["basomrade", "municipality", "county", "county_region", "country"]

            for i, entity in enumerate(entities):
                path = os.path.join(out_dir, "ddf--entities--{}.csv".format(entity_name[i]))
                print ("Printing " + path)
                entity.to_csv(path, index=False, encoding="utf-8")
                
        # Convert basomrade codes to IDs
        if (first_run):
            code_to_id = generate_code_dict(df_basomraden)
        data["basomrade"] = data["basomrade"].apply(lambda x: code_to_id[str(x)] if x != "" else "")
        
        print (" ------ Datapoints from sheet " + config["name"] + " ------ ")

        # DATAPOINTS
        if (not first_run):
            del df_dps_bas, df_dps_muni, df_dps_county, df_dps_county_r, df_dps_country
        df_dps_bas, df_dps_muni, df_dps_county, df_dps_county_r, df_dps_country =         extract_datapoints(data, df_basomraden, df_municipalities, df_counties, df_county_regions, df_countries)

        dps_all = [df_dps_bas, df_dps_muni, df_dps_county, df_dps_county_r, df_dps_country]

        for i, dps in enumerate(dps_all):
            measures = []
            measures = dps.columns[2:]
            for measure in measures:
                if (not first_run):
                    del df_datapoints
                df_datapoints = dps[[entity_name[i], "year"] + [measure]]
                # Exclude all null columns
                df_datapoints = df_datapoints.dropna(axis=0, how="any")
                if (not df_datapoints[measure].isnull().values.all()):
                    path = os.path.join(out_dir, "ddf--datapoints--{}--by--{}--year.csv".format(measure, entity_name[i]))
                    print ("Printing " + path)
                    df_datapoints.to_csv(path, index=False, encoding="utf-8")    
    
        # CONCEPTS
        if (first_run):
            concept_file = os.path.join(out_dir, "ddf--concepts.csv")
            if(os.path.isfile(concept_file)):
                os.remove(concept_file)
        if (not first_run):
            del df_concepts 
        print (" ------ Concepts from sheet " + config["name"] + " ------ ")
        df_concepts = extract_concepts(measures, column_names)
        path = os.path.join(out_dir, "ddf--concepts.csv")
        print ("Printing " + path)
        df_concepts.to_csv(path, index=False, encoding="utf-8")
        
        first_run = False
    
    # CLEANUP
    del data, df_basomraden, df_municipalities, df_counties, df_county_regions, df_countries, df_concepts,        df_dps_bas, df_dps_muni, df_dps_county, df_dps_county_r, df_dps_country, e_data, df_datapoints, b_names

