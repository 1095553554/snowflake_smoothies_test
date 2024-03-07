# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


st.title(":cup_with_straw: Fruit Bar :cup_with_straw:")
st.write('Choose fruits in your smoothie')
session = get_active_session()
df = session.table("smoothies.public.fruit_options").select(col("fruit_name"))
order_name = st.text_input("Name on smothie:")
st.write("The name on your smoothie is ",order_name)
# st.dataframe(data=df,use_container_width=True)

ingredients = st.multiselect(
    "Choose up to 5 ingredients"
    ,df
    ,max_selections=5
)
if ingredients:
    # st.write(ingredients)
    # st.text(ingredients)
    ingredient_str = ''
    for i in ingredients:
        ingredient_str += i+" "
    # st.write(ingredient_str)
    insert_stm = "insert into smoothies.public.orders(ingredients,name_on_order) \
        values ('"+ingredient_str+"','" +order_name+"')"
    # st.write(insert_stm)
    insert_flag = st.button("Submit order")
    if insert_flag:
        session.sql(insert_stm).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

