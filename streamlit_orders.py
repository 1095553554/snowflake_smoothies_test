# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col,when_matched

st.title(":cup_with_straw: Pending orders :cup_with_straw:")
st.write('Orders that need to be filled')
session = get_active_session()
my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()

# st.dataframe(data=edit_df,use_container_width=True)
if my_dataframe:
    edit_df = st.experimental_data_editor(my_dataframe)
    submit_flag = st.button("submit")
    if submit_flag:
        st.success("submitted",icon="👍")
        try:
            og_dataset = session.table("smoothies.public.orders")
            edited_dataset = session.create_dataframe(edit_df)
            og_dataset.merge(edited_dataset
             , (og_dataset['order_uid'] == edited_dataset['order_uid'])
             , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
            )
        except:
            st.write("Something went wrong!")

