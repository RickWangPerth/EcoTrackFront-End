import psycopg2
import pandas as pd


# Connection parameters
param_dic = {
    "host": "localhost",
    "database": "emissions",
    "user": "postgres",
    "password": "pB1@ckburn"
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

    # Naturally we get a list of tupples
    tupples = cursor.fetchall()
    cursor.close()

    # We just need to turn it into a pandas dataframe
    df = pd.DataFrame(tupples, columns=column_names)
    return df


conn = connect(param_dic)
column_names = ["id", "sector", "state", "sc2", "sc3", "unit"]
# Execute the "SELECT *" query
df = postgresql_to_dataframe(
    conn, "select * from electricity_ref", column_names)
df.head()


def elecal(state, unit, Q_elec):
    for i in range(12):
        if unit == 'kWh':
            if df.iloc[i][0] == state:
                EF_2 = df.iloc[i][1]
                EF_3 = df.iloc[i][3]
                print(state)
        if unit == 'GJ':
            if df.iloc[i][0] == state:
                EF_2 = df.iloc[i][2]
                EF_3 = df.iloc[i][4]
                print(state)
    elec_e = float(Q_elec) * (EF_2 + EF_3) / 1000
    return elec_e


Q_elec = 11300000  # INPUT FROM FRONT END - ENERGY USAGE
state = 'National'       # INPUT FROM FRONT END - STATE
unit = 'kWh'

emissions = elecal(state, unit, Q_elec)
print(emissions)
