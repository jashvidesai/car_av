# first separate families from not
import csv
import random
import pandas as pd


# Get the filename from user input
file_name = input("Enter the CSV filename: ")

# Read the CSV file
with open(file_name, 'r') as file:
  people_file = csv.reader(file)

  family_entries = []
  non_family_entries = []
  institutionalized_quarters_entries = []
  non_institutionalized_quarters_entries = []

  for row in people_file:
    if row[6] == '0':
      family_entries.append(row)
    if row[6] == '1':
      non_family_entries.append(row)
    if row[6] in ['2', '3', '4', '5']:
      institutionalized_quarters_entries.append(row)
    if row[6] in ['6', '7', '8']:
      non_institutionalized_quarters_entries.append(row)

  # deal with families first since this is a case of averaged income
  family_dict = {}
  for row in family_entries:
    fam_id = row[5]
    if fam_id in family_dict:
      family_dict[fam_id].append(row)
    else:
      family_dict[fam_id] = [row]

  # now, add characteristics to each family household
  for key, value in family_dict.items():
    # first is income, take the avg
    income_brackets = [
      {'name': '0.0', 'min_value': 0.00, 'max_value': 9999.99},
      {'name': '1.0', 'min_value': 10000.00, 'max_value': 14999.99},
      {'name': '2.0', 'min_value': 15000.00, 'max_value': 24999.99},
      {'name': '3.0', 'min_value': 25000.00, 'max_value': 34999.99},
      {'name': '4.0', 'min_value': 35000.00, 'max_value': 49999.99},
      {'name': '5.0', 'min_value': 50000.00, 'max_value': 74999.99},
      {'name': '6.0', 'min_value': 75000.00, 'max_value': 99999.99},
      {'name': '7.0', 'min_value': 100000.00, 'max_value': 149999.99},
      {'name': '8.0', 'min_value': 150000.00, 'max_value': 199999.99},
      {'name': '9.0', 'min_value': 200000.00, 'max_value': float('inf')}]
    
    # calculate avg and replace the 15th entry
    family_avg = sum(float(row[14]) for row in value) / len(value)
    for row in value:
      row[14] = str(round(family_avg, 2))

    # now replace the 14th entry
    for bracket in income_brackets:
      if bracket['min_value'] <= family_avg <= bracket['max_value']:
        family_income_bracket = bracket['name']
        break
    for row in value:
      row[13] = family_income_bracket

    # next sorting thing is sorting by hierarchy.
    # eldest male over 22 gets the car first and then the order is from oldest to youngest
    # assume that 0 is female, 1 is male
    
    value.sort(key=lambda row: int(row[10]), reverse = True) #sort by age
    criteria_rows = [row for row in value if row[11] == "1" and float(row[10]) >= 22]
    if criteria_rows:
      criteria_rows.sort(key=lambda row: float(row[10]), reverse=True)
      value.remove(criteria_rows[0])
      value.insert(0, criteria_rows[0])

    # count the number of people in each family
    num_people = len(value)
    for row in value:
      row.append(str(num_people))

    # count the number of drivers (>= 18) in the family
    num_drivers = sum(1 for row in value if int(row[10]) >= 18)
    for row in value:
      row.append(str(num_drivers))

  # now that households are created, assign a certain number of cars to each household based on family size and avg income
  for key, value in family_dict.items():
    first_row = value[0] # first member
    second_row = value[1] if len(value) > 1 else None # second member
    third_row = value[2] if len(value) > 2 else None # third member
    fourth_row = value[3] if len(value) > 3 else None # fourth member
    fifth_row = value[4] if len(value) > 4 else None # fifth member
    sixth_row = value[5] if len(value) > 5 else None # sixth member
    seventh_row = value[6] if len(value) > 6 else None # seventh member
    eight_row = value[7] if len(value) > 7 else None # eight member
    ninth_row = value[8] if len(value) > 8 else None # ninth member
    tenth_row = value[9] if len(value) > 9 else None # tenth member

    num_of_cars = 0
    if first_row[15] == '1':
      num_of_cars = 1
    elif first_row[15] == '2' and first_row[13] in ['0.0', '1.0', '2.0']:
      num_of_cars = 1
    elif first_row[15] == '2' and first_row[13] in ['3.0', '4.0', '5.0', '6.0', '7.0', '8.0', '9.0']:
      num_of_cars = 2
    elif first_row[15] == '3' and first_row[13] in ['0.0', '1.0', '2.0']:
      num_of_cars = 1
    elif first_row[15] == '3' and first_row[13] in ['3.0', '4.0', '5.0']:
      num_of_cars = 2
    elif first_row[15] == '3' and first_row[13] in ['6.0', '7.0', '8.0', '9.0']:
      num_of_cars = 3
    elif first_row[15] == '4' and first_row[13] in ['0.0', '1.0']:
      num_of_cars = 1
    elif first_row[15] == '4' and first_row[13] in ['2.0', '3.0', '4.0', '5.0']:
      num_of_cars = 2
    elif first_row[15] == '4' and first_row[13] in ['6.0', '7.0']:
      num_of_cars = 3
    elif first_row[15] == '4' and first_row[13] in ['8.0', '9.0']:
      num_of_cars = 4
    elif first_row[15] == '5' and first_row[13] in ['0.0', '1.0']:
      num_of_cars = 1
    elif first_row[15] == '5' and first_row[13] in ['2.0', '3.0', '4.0', '5.0']:
      num_of_cars = 2
    elif first_row[15] == '5' and first_row[13] in ['6.0', '7.0']:
      num_of_cars = 3
    elif first_row[15] == '5' and first_row[13] in ['8.0']:
      num_of_cars = 4
    elif first_row[15] == '5' and first_row[13] in ['9.0']:
      num_of_cars = 5
    elif first_row[15] in ['6', '7', '8', '9', '10'] and first_row[13] in ['0.0', '1.0', '2.0']:
      num_of_cars = 1
    elif first_row[15] in ['6', '7', '8', '9', '10'] and first_row[13] in ['3.0', '4.0']:
      num_of_cars = 2
    elif first_row[15] in ['6', '7', '8', '9', '10'] and first_row[13] in ['5.0', '6.0']:
      num_of_cars = 3
    elif first_row[15] in ['6', '7', '8', '9', '10'] and first_row[13] in ['7.0', '8.0', '9.0']:
      num_of_cars = 4

    for row in value:
      row.append(str(num_of_cars))

    # finally, rank household position
    for family_rank, row in enumerate(value, start=1):
      row.insert(1, family_rank)

# Assuming num_of_cars is an integer, not a string. If it's a string, convert it to int before this point.
    for row in value:
      row.extend([0.0, 0.0, 0.0, 0.0])
    
    for row in value:
      age = int(row[11])
      family_size = int(first_row[16])
      number_of_drivers = int(first_row[17])
      num_of_cars = int(first_row[18])

      # Case 1: absolute case #1, ages of 5 - 17 or 65 - 75
      if 5 <= age <= 17 or 66 <= age <= 75:
        row[19] = 0.00
        if first_row[14] in ['0.0', '1.0', '2.0', '3.0', '4.0']:
          row[22] = round(random.uniform(0.75, 0.85), 3)
          row[20] = round((1 - row[22]) * 0.7, 3)
          row[21] = round((1 - row[22]) * 0.3, 3)
        elif first_row[14] in ['5.0', '6.0', '7.0', '8.0', '9.0']:
          row[22] = round(random.uniform(0.75, 0.85), 3)
          row[20] = round((1 - row[22]) * 0.6, 3)
          row[21] = round((1 - row[22]) * 0.4, 3)

      # Case 2: absolute case #2, ages of 0 - 5 or 75+
      elif (0 <= age < 5) or (age > 75):
        row[19] = 0.0
        row[20] = 0.0
        row[21] = 0.0
        row[22] = 0.0
      
      # Case 3, start with ages and everyone has a car
      elif 18 <= age <= 65:
        if num_of_cars >= number_of_drivers:
          row[19] = round(random.uniform(0.9, 1.0), 3)
          if first_row[14] in ['0.0', '1.0', '2.0', '3.0', '4.0']:
            row[20] = round((1 - row[19]) * 0.1, 3)
            row[21] = round((1 - row[19]) * 0.1, 3)
            row[22] = round((1 - row[19]) * 0.8, 3)
          elif first_row[14] in ['5.0', '6.0', '7.0', '8.0', '9.0']:
            row[20] = round((1 - row[19]) * 0.2, 3)
            row[21] = round((1 - row[19]) * 0.2, 3)
            row[22] = round((1 - row[19]) * 0.6, 3)

      # Case 4: there are fewer cars than people in the family
        else:
          if row[1] <= num_of_cars:
            if num_of_cars == 1:
              for row in value[0:1]:
                row[19] = round(random.uniform((2.5/(2.5 + (number_of_drivers - 1))) - 0.05, 
                                                          (2.5/(2.5 + (number_of_drivers - 1))) + 0.05), 3)
                if row[14] in ['0.0', '1.0', '2.0', '3.0', '4.0']:
                  row[20] = round((1 - row[19]) * 0.1, 3)
                  row[21] = round((1 - row[19]) * 0.1, 3)
                  row[22] = round((1 - row[19]) * 0.8, 3)
                elif row[14] in ['5.0', '6.0', '7.0', '8.0', '9.0']:
                  row[20] = round((1 - row[19]) * 0.2, 3)
                  row[21] = round((1 - row[19]) * 0.2, 3)
                  row[22] = round((1 - row[19]) * 0.6, 3)

            # rest of drivers
              for row in value[1:]:
                row[19] = round(random.uniform((1/(2.5 + (number_of_drivers - 1))) - 0.05, 
                                                 (1/(2.5 + (number_of_drivers - 1))) + 0.05), 3)
                if row[14] in ['0.0', '1.0', '2.0', '3.0', '4.0']:
                  row[20] = round((1 - row[19]) * 0.1, 3)
                  row[21] = round((1 - row[19]) * 0.1, 3)
                  row[22] = round((1 - row[19]) * 0.8, 3)
                elif row[14] in ['5.0', '6.0', '7.0', '8.0', '9.0']:
                  row[20] = round((1 - row[19]) * 0.2, 3)
                  row[21] = round((1 - row[19]) * 0.2, 3)
                  row[22] = round((1 - row[19]) * 0.6, 3)
            elif num_of_cars == 2:
              for row in value[0:2]:
                row[19] = round(random.uniform((2.5/(5 + (number_of_drivers - 2))) - 0.05, 
                                                          (2.5/(5 + (number_of_drivers - 2))) + 0.05), 3)
                if row[14] in ['0.0', '1.0', '2.0', '3.0', '4.0']:
                  row[20] = round((1 - row[19]) * 0.1, 3)
                  row[21] = round((1 - row[19]) * 0.1, 3)
                  row[22] = round((1 - row[19]) * 0.8, 3)
                elif row[14] in ['5.0', '6.0', '7.0', '8.0', '9.0']:
                  row[20] = round((1 - row[19]) * 0.2, 3)
                  row[21] = round((1 - row[19]) * 0.2, 3)
                  row[22] = round((1 - row[19]) * 0.6, 3)

              # rest of drivers
              for row in value[2:]:
                row[19] = round(random.uniform((1/(5 + (number_of_drivers - 2))) - 0.05, 
                                                            (1/(5 + (number_of_drivers - 2))) + 0.05), 3)
                if row[14] in ['0.0', '1.0', '2.0', '3.0', '4.0']:
                  row[20] = round((1 - row[19]) * 0.1, 3)
                  row[21] = round((1 - row[19]) * 0.1, 3)
                  row[22] = round((1 - row[19]) * 0.8, 3)
                elif row[14] in ['5.0', '6.0', '7.0', '8.0', '9.0']:
                  row[20] = round((1 - row[19]) * 0.2, 3)
                  row[21] = round((1 - row[19]) * 0.2, 3)
                  row[22] = round((1 - row[19]) * 0.6, 3)

            elif num_of_cars == 3:
              for row in value[0:3]:
                row[19] = round(random.uniform((2.5/(7.5 + (number_of_drivers - 3))) - 0.05, 
                                                          (2.5/(7.5 + (number_of_drivers - 3))) + 0.05), 3)
                if row[14] in ['0.0', '1.0', '2.0', '3.0', '4.0']:
                  row[20] = round((1 - row[19]) * 0.1, 3)
                  row[21] = round((1 - row[19]) * 0.1, 3)
                  row[22] = round((1 - row[19]) * 0.8, 3)
                elif row[14] in ['5.0', '6.0', '7.0', '8.0', '9.0']:
                  row[20] = round((1 - row[19]) * 0.2, 3)
                  row[21] = round((1 - row[19]) * 0.2, 3)
                  row[22] = round((1 - row[19]) * 0.6, 3)

              # rest of drivers
              for row in value[3:]:
                row[19] = round(random.uniform((1/(7.5 + (number_of_drivers - 3))) - 0.05, 
                                                          (1/(7.5 + (number_of_drivers - 3))) + 0.05), 3)
                if row[14] in ['0.0', '1.0', '2.0', '3.0', '4.0']:
                  row[20] = round((1 - row[19]) * 0.1, 3)
                  row[21] = round((1 - row[19]) * 0.1, 3)
                  row[22] = round((1 - row[19]) * 0.8, 3)
                elif row[14] in ['5.0', '6.0', '7.0', '8.0', '9.0']:
                  row[20] = round((1 - row[19]) * 0.2, 3)
                  row[21] = round((1 - row[19]) * 0.2, 3)
                  row[22] = round((1 - row[19]) * 0.6, 3)

            elif num_of_cars == 4:
              for row in value[0:4]:
                row[19] = round(random.uniform((2.5/(10 + (number_of_drivers - 4))) - 0.05, 
                                                          (2.5/(10 + (number_of_drivers - 4))) + 0.05), 3)
                if row[14] in ['0.0', '1.0', '2.0', '3.0', '4.0']:
                  row[20] = round((1 - row[19]) * 0.1, 3)
                  row[21] = round((1 - row[19]) * 0.1, 3)
                  row[22] = round((1 - row[19]) * 0.8, 3)
                elif row[14] in ['5.0', '6.0', '7.0', '8.0', '9.0']:
                  row[20] = round((1 - row[19]) * 0.2, 3)
                  row[21] = round((1 - row[19]) * 0.2, 3)
                  row[22] = round((1 - row[19]) * 0.6, 3)

              # rest of drivers
              for row in value[4:]:
                row[19] = round(random.uniform((1/(10 + (number_of_drivers - 4))) - 0.05, 
                                                          (1/(10 + (number_of_drivers - 4))) + 0.05), 3)
                if row[14] in ['0.0', '1.0', '2.0', '3.0', '4.0']:
                  row[20] = round((1 - row[19]) * 0.1, 3)
                  row[21] = round((1 - row[19]) * 0.1, 3)
                  row[22] = round((1 - row[19]) * 0.8, 3)
                elif row[14] in ['5.0', '6.0', '7.0', '8.0', '9.0']:
                  row[20] = round((1 - row[19]) * 0.2, 3)
                  row[21] = round((1 - row[19]) * 0.2, 3)
                  row[22] = round((1 - row[19]) * 0.6, 3)

      # Append the probabilities list to the person's row
    
    for row in value:
      del row[1]
      del row[15]
      del row[16]
      del row[15]

    #print(f"Family ID: {key}")
    #print(f"Number of Cars: {num_of_cars}")
    #for row in value:
      #print(row)
    #print()

  # now, we deal with non-families
  non_family_dict = {}
  for row in non_family_entries:
    non_fam_id = row[5]
    if non_fam_id in non_family_dict:
      non_family_dict[non_fam_id].append(row)
    else:
      non_family_dict[non_fam_id] = [row]

  # now, add characteristics to each non-family household
  for key, value in non_family_dict.items():
    # count the number of people in the household and append it
    num_nonfam_people = len(value)
    for row in value:
      row.append(str(num_nonfam_people))

    total_num_of_cars = 0
    # treat everybody in the household like an individual and calculate car avail and probabilities based on age and income
    for row in value:
      num_of_cars = 0
      prob_drives_themselves = 0
      prob_gets_a_ride = 0
      prob_uses_uberormt = 0
      prob_uses_system2 = 0

      age = int(row[10])
      if (0 <= age <= 15):
        num_of_cars = 0
        prob_uses_system2 = round(random.uniform(0.9, 1.0), 3)
        prob_drives_themselves = 0.000
        prob_gets_a_ride = round((1 - prob_uses_system2) * 0.75, 3)
        prob_uses_uberormt = round((1 - prob_uses_system2) * 0.25, 3)

      elif (16 <= age <= 21):
        if row[13] in ['0.0', '1.0', '2.0', '3.0']:
          num_of_cars = 0
          prob_drives_themselves = 0.000
          prob_uses_system2 = round(random.uniform(0.9, 1.0), 3)
          prob_gets_a_ride = round((1 - prob_uses_system2) * 0.6, 3)
          prob_uses_uberormt = round((1 - prob_uses_system2) * 0.4, 3)
        if row[13] in ['4.0', '5.0', '6.0', '7.0', '8.0', '9.0']:
          num_of_cars = 1
          prob_drives_themselves = round(random.uniform(0.9, 1.0), 3)
          prob_gets_a_ride = round((1 - prob_drives_themselves) * 0.1, 3)
          prob_uses_uberormt = round((1 - prob_drives_themselves) * 0.2, 3)
          prob_uses_system2 = round((1 - prob_drives_themselves) * 0.7, 3)

      elif (22 <= age <= 65):
        if row[13] in ['0.0', '1.0']:
          num_of_cars = 0
          prob_drives_themselves = 0.000
          prob_uses_system2 = round(random.uniform(0.9, 1.0), 3)
          prob_gets_a_ride = round((1 - prob_uses_system2) * 0.6, 3)
          prob_uses_uberormt = round((1 - prob_uses_system2) * 0.4, 3)
        if row[13] in ['2.0', '3.0', '4.0', '5.0', '6.0']:
          num_of_cars = 1
          prob_drives_themselves = round(random.uniform(0.9, 1.0), 3)
          prob_gets_a_ride = round((1 - prob_drives_themselves) * 0.1, 3)
          prob_uses_uberormt = round((1 - prob_drives_themselves) * 0.1, 3)
          prob_uses_system2 = round((1 - prob_drives_themselves) * 0.8, 3)
        if row[13] in ['7.0', '8.0', '9.0']:
          num_of_cars = 2
          prob_drives_themselves = round(random.uniform(0.95, 1.0), 3)
          prob_gets_a_ride = round((1 - prob_drives_themselves) * 0.1, 3)
          prob_uses_uberormt = round((1 - prob_drives_themselves) * 0.2, 3)
          prob_uses_system2 = round((1 - prob_drives_themselves) * 0.7, 3)

      elif (age >= 66):
        if row[13] in ['0.0', '1.0', '2.0', '3.0', '4.0']:
          num_of_cars = 1
          prob_uses_system2 = round(random.uniform(0.9, 1.0), 3)
          prob_drives_themselves = 0.000
          prob_gets_a_ride = round((1 - prob_uses_system2) * 0.25, 3)
          prob_uses_uberormt = round((1 - prob_uses_system2) * 0.75, 3)
        if row[13] in ['5.0', '6.0', '7.0', '8.0', '9.0']:
          num_of_cars = 2
          prob_uses_system2 = round(random.uniform(0.95, 1.0), 3)
          prob_drives_themselves = 0.000
          prob_gets_a_ride = round((1 - prob_uses_system2) * 0.5, 3)
          prob_uses_uberormt = round((1 - prob_uses_system2) * 0.5, 3)
    
      row.append(prob_drives_themselves)
      row.append(prob_gets_a_ride)
      row.append(prob_uses_uberormt)
      row.append(prob_uses_system2)
      total_num_of_cars += num_of_cars

    for row in value:
      del row[15]

    #print(f"Non-Family ID: {key}")
    #print(f"Number of Cars: {total_num_of_cars}")
    #for row in value:
      #print(row)
    #print()

  # now, we deal with people in institutionalized quarters
  institutionalized_quarters_dict = {}
  for row in institutionalized_quarters_entries:
    institutionalized_quarters_id = row[5]
    if institutionalized_quarters_id in institutionalized_quarters_dict:
      institutionalized_quarters_dict[institutionalized_quarters_id].append(row)
    else:
      institutionalized_quarters_dict[institutionalized_quarters_id] = [row]

  # now, add characteristics to each institutionalized quarters household
  for key, value in institutionalized_quarters_dict.items():
    # count the number of people in the household and append it
    num_institutionalized_quarters = len(value)
    for row in value:
      row.append(str(num_institutionalized_quarters))

    total_num_of_cars = 0
    # treat everybody in the household like an individual and calculate car avail and probabilities based on age and income
    for row in value:
      num_of_cars = 0
      prob_drives_themselves = 0
      prob_gets_a_ride = 0
      prob_uses_uberormt = 0
      prob_uses_system3 = 0

      age = int(row[10])
      if (0 <= age < 65):
        num_of_cars = 0
        prob_drives_themselves = 0.00
        prob_gets_a_ride = round(random.uniform(0.00, 0.10), 3)
        prob_uses_system3 = round(0.9 * (1 - prob_gets_a_ride), 3)
        prob_uses_uberormt = round(0.1 * (1 - prob_gets_a_ride), 3)

      if (age >= 66):
        # correctional facilities (assumption)
        if row[13] in ['0.0', '1.0', '2.0', '3.0', '4.0']:
          num_of_cars = 0
          prob_drives_themselves = 0.00
          prob_uses_system3 = round(random.uniform(0.9, 1.0), 3)
          prob_uses_uberormt = round(0.5 * (1 - prob_uses_system3), 3)
          prob_gets_a_ride = round(0.5 * (1 - prob_uses_system3), 3)
        # nursing homes (assumption)
        if row[13] in ['5.0', '6.0', '7.0', '8.0', '9.0']:
          num_of_cars = 1
          prob_drives_themselves = 0.00
          prob_uses_system3 = round(random.uniform(0.5, 0.6), 3)
          prob_gets_a_ride = round(0.25 * (1 - prob_uses_system3), 3)
          prob_uses_uberormt = round(0.75 * (1 - prob_uses_system3), 3)

    for row in value:
      row.append(str(prob_drives_themselves))
      row.append(str(prob_gets_a_ride))
      row.append(str(prob_uses_uberormt))
      row.append(str(prob_uses_system3))
      total_num_of_cars += num_of_cars

    for row in value:
      del row[15]

    #print(f"Institutionalized Quarters Household ID: {key}")
    #print(f"Number of Cars: {total_num_of_cars}")
    #for row in value:
      #print(row)
    #print()

  # now, we deal with people in non-institutionalized quarters
  non_institutionalized_quarters_dict = {}
  for row in non_institutionalized_quarters_entries:
    non_institutionalized_quarters_id = row[5]
    if non_institutionalized_quarters_id in non_institutionalized_quarters_dict:
      non_institutionalized_quarters_dict[non_institutionalized_quarters_id].append(row)
    else:
      non_institutionalized_quarters_dict[non_institutionalized_quarters_id] = [row]

  # now, add characteristics to each non-institutionalized quarters household
  for key, value in non_institutionalized_quarters_dict.items():
    # count the number of people in the household and append it
    num_non_institutionalized_quarters = len(value)
    for row in value:
      row.append(str(num_non_institutionalized_quarters))

    total_num_of_cars = 0
    # treat everybody in the household like an individual and calculate car avail and probabilities based on age and income
    for row in value:
      num_of_cars = 0
      prob_drives_themselves = 0
      prob_gets_a_ride = 0
      prob_uses_uberormt = 0
      prob_uses_system4 = 0

      age = int(row[10])
      if (0 <= age < 18):
        num_of_cars = 0
        prob_drives_themselves = 0.00
        prob_uses_system4 = round(random.uniform(0.9, 1.0), 3)
        prob_gets_a_ride = round((1 - prob_uses_system4) * 0.75, 3)
        prob_uses_uberormt = round((1 - prob_uses_system4) * 0.25, 3)

      if (18 <= age < 65):
        if row[13] in ['0.0', '1.0', '2.0', '3.0']:
          num_of_cars = 0
          prob_drives_themselves = 0.00
          prob_uses_system4 = round(random.uniform(0.9, 1.0), 3)
          prob_gets_a_ride = round((1 - prob_uses_system4) * 0.9, 3)
          prob_uses_uberormt = round((1 - prob_uses_system4) * 0.1, 3)
        if row[13] in ['4.0', '5.0', '6.0', '7.0', '8.0', '9.0']:
          num_of_cars = 1
          prob_drives_themselves = round(random.uniform(0.9, 1.0), 3)
          prob_uses_system4 = round((1 - prob_drives_themselves) * 0.7, 3)
          prob_gets_a_ride = round((1 - prob_drives_themselves) * 0.1, 3)
          prob_uses_uberormt = round((1 - prob_drives_themselves) * 0.2, 3)

      if (age >= 65):
        if row[13] in ['0.0', '1.0', '2.0', '3.0', '4.0']:
          num_of_cars = 1
          prob_uses_system4 = round(random.uniform(0.9, 1.0), 3)
          prob_drives_themselves = 0.00
          prob_gets_a_ride = round((1 - prob_uses_system4) * 0.75, 3)
          prob_uses_uberormt = round((1 - prob_uses_system4) * 0.25, 3)
        if row[13] in ['5.0', '6.0', '7.0', '8.0', '9.0']:
          num_of_cars = 1
          prob_uses_system4 = round(random.uniform(0.9, 1.0), 3)
          prob_drives_themselves = 0.00
          prob_gets_a_ride = round((1 - prob_uses_system4) * 0.5, 3)
          prob_uses_uberormt = round((1 - prob_uses_system4) * 0.5, 3)
    
    for row in value:
      row.append(str(prob_drives_themselves))
      row.append(str(prob_gets_a_ride))
      row.append(str(prob_uses_uberormt))
      row.append(str(prob_uses_system4))
      total_num_of_cars += num_of_cars

    for row in value:
      del row[15]

    #print(f"Non-Institutionalized Quarters Household ID: {key}")
    #print(f"Number of Cars: {total_num_of_cars}")
    #for row in value:
      #print(row)
    #print()

  # combine all the rows into a single list
  all_entries = family_entries + non_family_entries + institutionalized_quarters_entries + non_institutionalized_quarters_entries

  # convert the list of rows into a DataFrame
  columns = ['Counter', 'Residence State', 'County Code', 'Tract Code', 'Block Code', 'HH ID', 'HH Type', 'Latitude', 'Longitude', 
           'Person ID Number', 'Age', 'Sex', 'Traveler Type', 'Income Bracket (Avg for Family)', 'Income Amount (Avg for Family)',
           'Prob. of Driving Themselves', 'Prob. of Getting a Ride', 'Prob. of Using Uber/MT', 'Prob. of Taking AV System']
  df = pd.DataFrame(all_entries, columns=columns)

  # Save the DataFrame to an Excel file
  df.to_excel('all_data.xlsx', index=False)