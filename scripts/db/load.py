def insert_df(df, table):
    engine = get_engine()
    df.to_sql(table, engine, if_exists="append", index=False)