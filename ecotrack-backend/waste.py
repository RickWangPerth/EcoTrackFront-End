import psycopg2
import pandas as pd
import sys

host = 'postgres'
database = 'ecotrak'
user = 'postgres'
password = 'postgres'
table_name = 'wastes_ef'
column_names = ['id', 'name', 'unit', 'type', 'value',
                'scope', 'ratio', 'treatment']

# Connection parameters
param_dic = {
    "host": host,
    "database": database,
    "user": user,
    "password": password
}


def connect(params_dic):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params_dic)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1)
    print("Connection successful")
    return conn


def postgresql_to_dataframe(conn, select_query, column_names):
    """
    Tranform a SELECT query into a pandas dataframe
    """
    cursor = conn.cursor()
    try:
        cursor.execute(select_query)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return 1

    tupples = cursor.fetchall()
    cursor.close()

    df = pd.DataFrame(tupples, columns=column_names)
    return df


conn = connect(param_dic)
column_names = column_names
# Create Dataframe
df = postgresql_to_dataframe(
    conn, "select * from " + table_name, column_names)
df.head()

#name = 'Food'
# Solid Waste
solid_df = df.loc[df['type'] == 'Solid Waste']


def solid_kg(Q, name):
    EF = solid_df.loc[solid_df['name']
                      == name, 'value'].iloc[0]
    solid_e = Q * EF
    return solid_e


# Solid Waste - weight unknown
# n = 24
# m = 3


def solid_m3(Q, n, name):
    CF = solid_df.loc[solid_df['name']
                      == name, 'ratio'].iloc[0]
    EF = solid_df.loc[solid_df['name']
                      == name, 'value'].iloc[0]
    solid_e = Q * n * CF * EF
    return solid_e


# Waste water treatment

# def wastewater(P, EF):
#     waste_e = P * EF
#     return waste_e


# ex_11 = wastewater(20000, 0.3276)
# print("Total Greenhouse Gas Emissions from Example 11 (t CO2e): ", ex_11)

# # Waste incineration


def incineration(Q, name):
    EF = solid_df.loc[solid_df['name']
                      == name, 'value'].iloc[0]
    waste_e = Q * EF
    return waste_e


# def compost(Q, EF, R):
#     waste_e = Q * EF - R
#     return waste_e


# ex_13 = compost(0.13, 0.046, 0)
# print("Total Greenhouse Gas Emissions from Example 13    (t CO2e): ", ex_13)

def wastecal(Q, n, unit, type, subtype):
    if type == 'Solid Waste':
        if unit == 'kg':
            waste_e = solid_kg(Q, n, subtype)
        elif unit == 'm3':
            waste_e = solid_m3(Q, n, subtype)

    elif type == 'Combined Waste':
        waste_e = incineration(Q, subtype)
    return waste_e
