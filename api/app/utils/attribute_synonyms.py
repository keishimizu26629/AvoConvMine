ATTRIBUTE_SYNONYMS = {
    "job": ["Occupation", "Job", "Career", "Profession", "Employment", "Work", "Role"],
    "family": ["Family", "Relatives", "Parents", "Children", "Siblings", "Spouse"],
    "hobby": ["Hobby", "Interest", "Pastime", "Leisure activity", "Recreation"],
    "location": ["Location", "Address", "City", "Country", "Place"],
    "residence": ["Residence", "Home", "Living place", "Dwelling"],
    "workplace": ["Workplace", "Office", "Work location", "Business address"],
    # 他のカテゴリーも必要に応じて追加
}

LOCATION_PRIORITIES = {
    "live": ["Location Residence", "Residence", "Location"],
    "work": ["Location Workplace", "Workplace", "Location"]
}
