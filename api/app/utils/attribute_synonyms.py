ATTRIBUTE_SYNONYMS = {
    "job": ["Occupation", "Job", "Career", "Profession", "Employment", "Work", "Role"],
    "family": ["Family", "Relatives", "Parents", "Children", "Siblings", "Spouse", "Child", "Kids"],
    "hobby": ["Hobby", "Interest", "Pastime", "Leisure activity", "Recreation"],
    "location": ["Location", "Address", "City", "Country", "Place"],
    "residence": ["Residence", "Home", "Living place", "Dwelling", "Location", "Address"],
    "workplace": ["Workplace", "Office", "Work location", "Business address"],
    "children": ["Family_children", "Daughter", "Son", "Kids", "Offspring"],
    "student": ["student", "education", "school", "age_group", "grade"],
    # 他のカテゴリーも必要に応じて追加
}

LOCATION_PRIORITIES = {
    "live": ["Residence Prefecture", "Location", "Address"],
    "work": ["Occupation Location", "Workplace", "Location"]
}
