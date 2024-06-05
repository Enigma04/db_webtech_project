def kg_facility_helper(facility) -> dict:
    return {
        "id": str(facility["_id"]),
        "X": facility["X"],
        "Y": facility["Y"],
        "OBJECTID": facility["OBJECTID"],
        "ID": facility["ID"],
        "TRAEGER": facility["TRAEGER"],
        "BEZEICHNUNG": facility["BEZEICHNUNG"],
        "KURZBEZEICHNUNG": facility["KURZBEZEICHNUNG"],
        "STRASSE": facility["STRASSE"],
        "STRSCHL": facility["STRSCHL"],
        "HAUSBEZ": facility["HAUSBEZ"],
        "PLZ": facility["PLZ"],
        "ORT": facility["ORT"],
        "HORT": facility["HORT"],
        "KITA": facility["KITA"],
        "TELEFON": facility.get("TELEFON", ""),
        "EMAIL": facility.get("EMAIL", ""),
        "BARRIEREFREI": facility["BARRIEREFREI"],
        "INTEGRATIV": facility["INTEGRATIV"]
    }


def school_facility_helper(facility) -> dict:
    return {
        "id": str(facility["_id"]),
        "X": facility["X"],
        "Y": facility["Y"],
        "OBJECTID": facility["OBJECTID"],
        "ID": facility["ID"],
        "TYP": facility["TYP"],
        "ART": facility["ART"],
        #"STANDORTTYP": facility["STANDORTTYP"],
        "BEZEICHNUNG": facility["BEZEICHNUNG"],
        "KURZBEZEICHNUNG": facility["KURZBEZEICHNUNG"],
        "STRASSE": facility["STRASSE"],
        "PLZ": facility["PLZ"],
        "ORT": facility["ORT"],
        "TELEFON": facility.get("TELEFON", ""),
        "FAX": facility.get("FAX", ""),
        "EMAIL": facility.get("EMAIL", ""),
        "PROFILE": facility.get("PROFILE", ""),
        "WWW": facility.get("WWW", ""),
        "TRAEGER": facility["TRAEGER"],
        "TRAEGERTYP": facility["TRAEGERTYP"],
        #"BEZUGNR": facility["BEZUGNR"],
        "GEBIETSARTNUMMER": facility["GEBIETSARTNUMMER"],
        "SNUMMER": facility["SNUMMER"],
        "NUMMER": facility["NUMMER"],
        "GlobalID": str(facility["GlobalID"])
    }


def sp_facility_helper(facility) -> dict:
    return {
        "id": str(facility["_id"]),
        "X": facility["X"],
        "Y": facility["Y"],
        "OBJECTID": facility["OBJECTID"],
        "ID": facility["ID"],
        "TRAEGER": facility["TRAEGER"],
        "LEISTUNGEN": facility["LEISTUNGEN"],
        "STRASSE": facility["STRASSE"],
        "PLZ": facility["PLZ"],
        "ORT": facility["ORT"],
        #"TELEFON": facility["TELEFON"]
    }
